from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# These are module-level variables set during app startup (see main.py lifespan).
# They start as None and are populated before any request can arrive.
engine: AsyncEngine | None = None
AsyncSessionLocal: sessionmaker | None = None


# Base is the parent class all SQLAlchemy models will inherit from.
# We define it here so models can import it in Phase 2.
class Base(DeclarativeBase):
    pass


async def init_postgres() -> None:
    """Create the async engine. Called once at startup."""
    global engine, AsyncSessionLocal

    # echo=False keeps SQL out of the logs; flip to True to see every query.
    engine = create_async_engine(settings.postgres_url, echo=False)

    # A sessionmaker is a factory for database sessions.
    # expire_on_commit=False keeps ORM objects usable after a commit.
    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )


async def close_postgres() -> None:
    """Dispose all connections in the pool. Called at shutdown."""
    if engine:
        await engine.dispose()


async def get_db():
    """
    FastAPI dependency — yields a database session for a single request,
    then closes it automatically when the request is done.

    Usage in a route:
        async def my_route(db: AsyncSession = Depends(get_db)): ...
    """
    async with AsyncSessionLocal() as session:
        yield session
