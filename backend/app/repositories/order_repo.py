"""
Order creation is where Postgres and MongoDB meet, and where transactions matter.

The flow for placing an order:
  1. Look up each product in MongoDB → get current name and price
  2. Lock each inventory row with SELECT ... FOR UPDATE
  3. Verify stock is sufficient for every item
  4. Decrement stock, INSERT order + line items — all in one Postgres transaction

Steps 2-4 are atomic. Two concurrent checkouts for the last item in stock will
queue at step 2: the second request waits until the first commits or rolls back,
then re-reads the (now-decremented) stock. This is how we prevent overselling.

The CHECK (stock >= 0) on the inventory table is a second line of defense: even
if application logic has a bug, Postgres will reject the update.
"""

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db_models.inventory import Inventory
from app.db_models.order import Order, OrderItem
from app.models.order import OrderCreate, OrderOut
from app.repositories import product_repo


async def create(db: AsyncSession, data: OrderCreate) -> OrderOut:
    # ── Step 1: Resolve each product from MongoDB ─────────────────────────────
    items_data: list[dict] = []
    total = Decimal("0")

    for item_in in data.items:
        product = await product_repo.get_by_id(item_in.product_id)
        if product is None:
            raise ValueError(f"Product '{item_in.product_id}' not found in catalog")

        unit_price = Decimal(str(product.price))
        subtotal = unit_price * item_in.quantity
        total += subtotal

        items_data.append({
            "product_id": item_in.product_id,
            "product_name": product.name,
            "quantity": item_in.quantity,
            "unit_price": unit_price,
            "subtotal": subtotal,
        })

    # ── Step 2: Lock inventory rows (SELECT ... FOR UPDATE) ───────────────────
    # with_for_update() tells Postgres to acquire a row-level exclusive lock.
    # Any other transaction trying to lock the same row will block here until
    # we commit or roll back. This is what prevents the race condition:
    #
    #   T1 reads stock=1, T2 reads stock=1, both think it's fine, both decrement
    #   → stock=-1 (oversell, wrong)
    #
    # With FOR UPDATE, T2 waits for T1 to finish. T2 then reads stock=0 and fails.
    locked: dict[str, Inventory] = {}
    for item_in in data.items:
        result = await db.execute(
            select(Inventory)
            .where(Inventory.product_id == item_in.product_id)
            .with_for_update()
        )
        inv = result.scalar_one_or_none()
        if inv is None:
            raise ValueError(
                f"No inventory record for product '{item_in.product_id}'. "
                "Run seed_inventory.py or set stock via PUT /inventory/{product_id}."
            )
        locked[item_in.product_id] = inv

    # ── Step 3: Verify stock ───────────────────────────────────────────────────
    for item_in in data.items:
        inv = locked[item_in.product_id]
        product_name = next(
            d["product_name"] for d in items_data if d["product_id"] == item_in.product_id
        )
        if inv.stock < item_in.quantity:
            raise ValueError(
                f"Insufficient stock for '{product_name}': "
                f"{inv.stock} available, {item_in.quantity} requested"
            )

    # ── Step 4: Decrement stock + write order (one atomic commit) ─────────────
    for item_in in data.items:
        locked[item_in.product_id].stock -= item_in.quantity

    order = Order(
        user_id=data.user_id,
        status="pending",
        total_amount=total,
        items=[OrderItem(**item) for item in items_data],
    )
    db.add(order)
    await db.commit()  # locks released here; inventory + order written atomically

    return await get_by_id(db, order.id)


async def get_by_id(db: AsyncSession, order_id: int) -> OrderOut | None:
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()
    if order is None:
        return None
    return OrderOut.model_validate(order)
