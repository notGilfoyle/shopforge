"""
Seed script — populates the products collection with sample data.

Run from the backend/ directory:
    uv run python scripts/seed_products.py

Run with --reset to wipe existing products first:
    uv run python scripts/seed_products.py --reset

The data intentionally spans three categories with very different `attributes`
to show why MongoDB's flexible schema is a natural fit for a product catalog.
"""

import asyncio
import sys
from datetime import UTC, datetime

from motor.motor_asyncio import AsyncIOMotorClient

# Add backend/ to the path so we can import app modules
sys.path.insert(0, ".")

from app.config import settings

# ── Sample documents ──────────────────────────────────────────────────────────
# Notice: every product in the same collection, but `attributes` is completely
# different per category. In a relational DB this would require either
# separate tables or many nullable columns.

PRODUCTS = [
    {
        "name": 'Samsung 55" QLED TV',
        "description": "4K smart TV with quantum dot display and built-in streaming.",
        "price": 799.99,
        "category": "electronics",
        "inventory_count": 12,
        "attributes": {
            "brand": "Samsung",
            "screen_size_inches": 55,
            "resolution": "4K",
            "smart_tv": True,
            "hdmi_ports": 4,
            "refresh_rate_hz": 120,
        },
        "images": [],
    },
    {
        "name": "Sony WH-1000XM5 Headphones",
        "description": "Industry-leading noise cancelling with 30-hour battery life.",
        "price": 349.99,
        "category": "electronics",
        "inventory_count": 35,
        "attributes": {
            "brand": "Sony",
            "wireless": True,
            "noise_cancellation": True,
            "battery_hours": 30,
            "foldable": True,
        },
        "images": [],
    },
    {
        "name": "Fluent Python, 2nd Edition",
        "description": "Clear, concise, and effective Python programming.",
        "price": 59.99,
        "category": "books",
        "inventory_count": 50,
        "attributes": {
            "author": "Luciano Ramalho",
            "isbn": "978-1492056355",
            "pages": 1012,
            "publisher": "O'Reilly Media",
            "edition": 2,
            "language": "English",
        },
        "images": [],
    },
    {
        "name": "The Pragmatic Programmer",
        "description": "Your journey to mastery, 20th Anniversary Edition.",
        "price": 49.99,
        "category": "books",
        "inventory_count": 28,
        "attributes": {
            "author": "David Thomas, Andrew Hunt",
            "isbn": "978-0135957059",
            "pages": 352,
            "publisher": "Addison-Wesley",
            "edition": 2,
            "language": "English",
        },
        "images": [],
    },
    {
        "name": "Classic Cotton T-Shirt",
        "description": "Everyday staple, pre-shrunk ring-spun cotton.",
        "price": 24.99,
        "category": "clothing",
        "inventory_count": 200,
        "attributes": {
            "material": "100% ring-spun cotton",
            "sizes_available": ["XS", "S", "M", "L", "XL", "XXL"],
            "color_options": ["white", "black", "navy", "charcoal"],
            "care": "Machine wash cold, tumble dry low",
            "fit": "unisex regular",
        },
        "images": [],
    },
]


async def seed(reset: bool = False) -> None:
    client = AsyncIOMotorClient(settings.mongo_url)
    db = client[settings.mongo_db_name]
    collection = db["products"]

    if reset:
        await collection.delete_many({})
        print("✓ Cleared existing products")

    now = datetime.now(UTC)
    docs = [{"created_at": now, "updated_at": now, **p} for p in PRODUCTS]
    result = await collection.insert_many(docs)
    print(f"✓ Inserted {len(result.inserted_ids)} products")

    # Print the category breakdown to make the flexible schema visible
    print("\nProducts by category:")
    async for doc in collection.aggregate([
        {"$group": {"_id": "$category", "count": {"$sum": 1}}}
    ]):
        print(f"  {doc['_id']}: {doc['count']}")

    client.close()


if __name__ == "__main__":
    reset_flag = "--reset" in sys.argv
    asyncio.run(seed(reset=reset_flag))
