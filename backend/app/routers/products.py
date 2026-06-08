from fastapi import APIRouter, HTTPException, Query

from app.models.product import ProductCreate, ProductOut, ProductUpdate
from app.repositories import product_repo as repo

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=ProductOut, status_code=201)
async def create_product(body: ProductCreate):
    """Insert a new product into the catalog."""
    return await repo.create(body)


@router.get("", response_model=list[ProductOut])
async def list_products(
    category: str | None = Query(None, description="Filter by category"),
    skip: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(20, ge=1, le=100, description="Max results to return"),
):
    """
    List products, optionally filtered by category.
    Supports basic pagination with skip/limit.
    """
    return await repo.list_all(category=category, skip=skip, limit=limit)


@router.get("/{id}", response_model=ProductOut)
async def get_product(id: str):
    """Fetch a single product by its MongoDB ObjectId."""
    product = await repo.get_by_id(id)
    if not product:
        # get_by_id returns None for both invalid IDs and missing documents.
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{id}", response_model=ProductOut)
async def update_product(id: str, body: ProductUpdate):
    """
    Partially update a product. Only the fields you include in the request
    body are changed — the rest stay as-is.
    """
    product = await repo.update(id, body)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{id}", status_code=204)
async def delete_product(id: str):
    """Remove a product from the catalog. Returns 204 No Content on success."""
    deleted = await repo.delete(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
