from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.mongo import close_mongo, init_mongo
from app.database.postgres import close_postgres, init_postgres
from app.repositories import product_repo, review_repo
from app.routers import health, inventory, orders, products, reviews, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    The lifespan context manager is FastAPI's way of running startup/shutdown logic.
    Code before `yield` runs on startup; code after runs on shutdown.
    This replaces the older @app.on_event("startup") decorator pattern.
    """
    # ── Startup ───────────────────────────────────────────────────────────────
    await init_postgres()              # create the SQLAlchemy engine + connection pool
    await init_mongo()                 # connect the Motor client to MongoDB
    await product_repo.ensure_indexes()
    await review_repo.ensure_indexes()   # create MongoDB indexes if they don't exist
    print("✓ PostgreSQL and MongoDB connections established")

    yield  # the app runs here, handling requests

    # ── Shutdown ──────────────────────────────────────────────────────────────
    await close_postgres()  # drain the connection pool gracefully
    await close_mongo()     # close the MongoDB connection
    print("✓ Database connections closed")


app = FastAPI(
    title="ShopForge API",
    description="Learning project: FastAPI + PostgreSQL + MongoDB",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(inventory.router)
app.include_router(reviews.router)
