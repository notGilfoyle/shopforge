from fastapi import APIRouter, HTTPException, Query

from app.models.review import ReviewCreate, ReviewOut
from app.repositories import product_repo, review_repo

router = APIRouter(tags=["reviews"])


@router.post("/products/{product_id}/reviews", response_model=ReviewOut, status_code=201)
async def create_review(product_id: str, body: ReviewCreate):
    if not await product_repo.get_by_id(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return await review_repo.create(product_id, body)


@router.get("/products/{product_id}/reviews", response_model=list[ReviewOut])
async def list_reviews(
    product_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    return await review_repo.list_by_product(product_id, skip=skip, limit=limit)


@router.delete("/reviews/{review_id}", status_code=204)
async def delete_review(review_id: str):
    if not await review_repo.delete(review_id):
        raise HTTPException(status_code=404, detail="Review not found")
