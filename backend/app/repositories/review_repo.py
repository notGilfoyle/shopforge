"""
Reviews are stored as a separate MongoDB collection rather than embedded inside
product documents.

Embedding would look like:
    { _id: ..., name: "TV", reviews: [ {...}, {...} ] }

Referencing looks like (what we do):
    products:  { _id: "abc", name: "TV" }
    reviews:   { _id: "xyz", product_id: "abc", rating: 5, ... }

Why reference instead of embed here?
- Reviews are unbounded — a popular product could have thousands. MongoDB documents
  cap at 16 MB; an embedded array would eventually hit that limit.
- We might want to query reviews independently: "all reviews by user 42", "latest
  reviews across all products". Those queries are awkward against embedded arrays.
- Embedding makes sense for small, bounded sub-documents that are always read
  together with the parent (e.g., a product's spec sheet). Reviews aren't that.
"""

from datetime import UTC, datetime

from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorCollection

from app.database.mongo import get_mongo_db
from app.models.review import ReviewCreate, ReviewOut


def _collection() -> AsyncIOMotorCollection:
    return get_mongo_db()["reviews"]


def _to_object_id(id: str) -> ObjectId | None:
    try:
        return ObjectId(id)
    except InvalidId:
        return None


async def ensure_indexes() -> None:
    col = _collection()
    # The primary access pattern: "give me all reviews for product X, newest first"
    await col.create_index([("product_id", 1), ("created_at", -1)])


async def create(product_id: str, data: ReviewCreate) -> ReviewOut:
    doc = {
        "product_id": product_id,
        **data.model_dump(),
        "created_at": datetime.now(UTC),
    }
    result = await _collection().insert_one(doc)
    doc["_id"] = result.inserted_id
    return ReviewOut.model_validate(doc)


async def list_by_product(
    product_id: str,
    skip: int = 0,
    limit: int = 20,
) -> list[ReviewOut]:
    cursor = (
        _collection()
        .find({"product_id": product_id})
        .sort("created_at", -1)
        .skip(skip)
        .limit(limit)
    )
    return [ReviewOut.model_validate(doc) async for doc in cursor]


async def delete(review_id: str) -> bool:
    oid = _to_object_id(review_id)
    if oid is None:
        return False
    result = await _collection().delete_one({"_id": oid})
    return result.deleted_count == 1
