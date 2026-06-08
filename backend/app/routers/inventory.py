from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.postgres import get_db
from app.models.inventory import InventoryOut, InventorySet
from app.repositories import inventory_repo

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/{product_id}", response_model=InventoryOut)
async def get_inventory(product_id: str, db: AsyncSession = Depends(get_db)):
    inv = await inventory_repo.get(db, product_id)
    if inv is None:
        raise HTTPException(status_code=404, detail="No inventory record for this product")
    return inv


@router.put("/{product_id}", response_model=InventoryOut)
async def set_inventory(
    product_id: str, body: InventorySet, db: AsyncSession = Depends(get_db)
):
    return await inventory_repo.set_stock(db, product_id, body.stock)
