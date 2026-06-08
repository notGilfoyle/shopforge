from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import settings

# Module-level variables set at startup.
client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None


async def init_mongo() -> None:
    """Connect to MongoDB. Called once at startup."""
    global client, db

    client = AsyncIOMotorClient(settings.mongo_url)
    # `client[name]` selects (or lazily creates) a database by name.
    db = client[settings.mongo_db_name]


async def close_mongo() -> None:
    """Close the MongoDB connection. Called at shutdown."""
    if client:
        client.close()


def get_mongo_db() -> AsyncIOMotorDatabase:
    """
    Return the shared database handle.

    Usage in a route:
        mongo = get_mongo_db()
        products = await mongo["products"].find().to_list(100)
    """
    return db
