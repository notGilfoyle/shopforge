from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_models.inventory import Inventory
from app.models.inventory import InventoryOut


async def get(db: AsyncSession, product_id: str) -> InventoryOut | None:
    result = await db.execute(
        select(Inventory).where(Inventory.product_id == product_id)
    )
    inv = result.scalar_one_or_none()
    return InventoryOut.model_validate(inv) if inv else None


async def set_stock(db: AsyncSession, product_id: str, stock: int) -> InventoryOut:
    result = await db.execute(
        select(Inventory).where(Inventory.product_id == product_id)
    )
    inv = result.scalar_one_or_none()
    if inv is None:
        inv = Inventory(product_id=product_id, stock=stock)
        db.add(inv)
    else:
        inv.stock = stock
    await db.commit()
    await db.refresh(inv)
    return InventoryOut.model_validate(inv)
