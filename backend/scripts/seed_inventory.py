"""
Seed inventory for every product in the MongoDB catalog.

Usage:
    uv run python scripts/seed_inventory.py           # skip products already in inventory
    uv run python scripts/seed_inventory.py --reset   # clear all inventory first
"""

import asyncio
import sys

from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, ".")

from app.config import settings
from app.db_models.inventory import Inventory

DEFAULT_STOCK = 50


async def seed() -> None:
    reset = "--reset" in sys.argv

    # Pull product IDs + names from MongoDB
    mongo_client = AsyncIOMotorClient(settings.mongo_url)
    products = await (
        mongo_client[settings.mongo_db_name]["products"]
        .find({}, {"_id": 1, "name": 1})
        .to_list(length=None)
    )
    mongo_client.close()

    if not products:
        print("No products found in MongoDB. Run seed_products.py first.")
        return

    engine = create_async_engine(settings.postgres_url)
    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with Session() as session:
        if reset:
            await session.execute(text("DELETE FROM inventory"))
            await session.commit()
            print("Cleared existing inventory.\n")

        seeded = skipped = 0
        for p in products:
            product_id = str(p["_id"])
            name = p.get("name", product_id)

            existing = (
                await session.execute(
                    select(Inventory).where(Inventory.product_id == product_id)
                )
            ).scalar_one_or_none()

            if existing:
                print(f"  ~ {name}: already has {existing.stock} units, skipped")
                skipped += 1
            else:
                session.add(Inventory(product_id=product_id, stock=DEFAULT_STOCK))
                print(f"  + {name}: {DEFAULT_STOCK} units")
                seeded += 1

        await session.commit()

    await engine.dispose()
    print(f"\nDone. Seeded: {seeded}, Skipped: {skipped}")


if __name__ == "__main__":
    asyncio.run(seed())
