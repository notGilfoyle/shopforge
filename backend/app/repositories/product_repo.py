"""
All MongoDB operations for the products collection live here.

Keeping DB logic out of the router means routes stay thin
(validate input → call repo → return result) and the queries
are easy to find and test in one place.
"""

from datetime import UTC, datetime

from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorCollection

from app.database.mongo import get_mongo_db
from app.models.product import ProductCreate, ProductOut, ProductUpdate


def _collection() -> AsyncIOMotorCollection:
    """Returns the 'products' collection from the shared Motor database handle."""
    return get_mongo_db()["products"]


def _to_object_id(id: str) -> ObjectId | None:
    """Convert a string to ObjectId. Returns None if the string isn't a valid id."""
    try:
        return ObjectId(id)
    except InvalidId:
        return None


async def ensure_indexes() -> None:
    """
    Create indexes once at startup. MongoDB only does work if the index
    doesn't exist yet, so this is safe to call on every boot.
    """
    col = _collection()
    # category index speeds up GET /products?category=electronics
    await col.create_index("category")
    # text index lets MongoDB do basic keyword search across name + description
    await col.create_index([("name", "text"), ("description", "text")])


# ── Create ────────────────────────────────────────────────────────────────────

async def create(data: ProductCreate) -> ProductOut:
    doc = data.model_dump()
    now = datetime.now(UTC)
    doc["created_at"] = now
    doc["updated_at"] = now

    result = await _collection().insert_one(doc)
    # insert_one returns just the inserted id; fetch the full document to return.
    return await get_by_id(str(result.inserted_id))


# ── Read ──────────────────────────────────────────────────────────────────────

async def get_by_id(id: str) -> ProductOut | None:
    oid = _to_object_id(id)
    if oid is None:
        return None
    doc = await _collection().find_one({"_id": oid})
    if doc is None:
        return None
    return ProductOut.model_validate(doc)


async def list_all(
    category: str | None = None,
    skip: int = 0,
    limit: int = 20,
) -> list[ProductOut]:
    query: dict = {}
    if category:
        # exact match for now; could extend to regex or $in later
        query["category"] = category

    cursor = _collection().find(query).skip(skip).limit(limit)
    docs = await cursor.to_list(limit)
    return [ProductOut.model_validate(doc) for doc in docs]


# ── Update ────────────────────────────────────────────────────────────────────

async def update(id: str, data: ProductUpdate) -> ProductOut | None:
    oid = _to_object_id(id)
    if oid is None:
        return None

    # Drop None values — we only $set fields the caller actually provided.
    changes = {k: v for k, v in data.model_dump().items() if v is not None}
    if changes:
        changes["updated_at"] = datetime.now(UTC)
        await _collection().update_one({"_id": oid}, {"$set": changes})

    return await get_by_id(id)


# ── Delete ────────────────────────────────────────────────────────────────────

async def delete(id: str) -> bool:
    oid = _to_object_id(id)
    if oid is None:
        return False
    result = await _collection().delete_one({"_id": oid})
    return result.deleted_count == 1
