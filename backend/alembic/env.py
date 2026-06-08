import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Load our app config so Alembic uses the same DB URL as the app.
from app.config import settings
from app.database.postgres import Base

# These imports look unused but they're not — importing the modules causes
# the SQLAlchemy models to register themselves on Base.metadata, which is
# what Alembic inspects when auto-generating migrations.
import app.db_models.user       # noqa: F401
import app.db_models.order      # noqa: F401
import app.db_models.inventory  # noqa: F401

# Standard Alembic boilerplate — reads alembic.ini for logging config.
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Override the URL from alembic.ini with our app's settings.
# Single source of truth: change the URL in config.py, not in two places.
config.set_main_option("sqlalchemy.url", settings.postgres_url)

# target_metadata tells Alembic what the schema *should* look like.
# It compares this to the live database to generate the migration diff.
target_metadata = Base.metadata


# ── Offline mode ──────────────────────────────────────────────────────────────
# Generates SQL to a file without connecting to the database.
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


# ── Online mode ───────────────────────────────────────────────────────────────
# Connects to the database and applies migrations directly.
def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # no connection pooling during migrations
    )
    async with connectable.connect() as connection:
        # run_sync bridges async SQLAlchemy into Alembic's sync migration API
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
