from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.postgres import get_db
from app.models.order import OrderCreate, OrderOut
from app.repositories import order_repo

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut, status_code=201)
async def create_order(body: OrderCreate, db: AsyncSession = Depends(get_db)):
    """
    Place an order. This is the cross-database moment:
      - Reads product name + price from MongoDB
      - Writes the order + line items to PostgreSQL in one transaction

    Note: if MongoDB is reachable but Postgres fails after the reads,
    no order is created (Postgres rolls back). MongoDB is never written to
    here, so there's nothing to undo on that side.
    """
    try:
        return await order_repo.create(db, body)
    except ValueError as exc:
        # order_repo raises ValueError when a product_id doesn't exist
        raise HTTPException(status_code=422, detail=str(exc))


@router.get("/{order_id}", response_model=OrderOut)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await order_repo.get_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
