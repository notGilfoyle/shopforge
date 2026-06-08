"""
SQLAlchemy ORM model for the users table.

This is the table definition — it tells SQLAlchemy (and Alembic) exactly
what columns exist, their types, and their constraints.

Naming note:
  app/db_models/ — SQLAlchemy models  (what the database looks like)
  app/models/    — Pydantic schemas    (what the API accepts/returns)
"""

from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.postgres import Base


class User(Base):
    __tablename__ = "users"

    # SERIAL PRIMARY KEY — PostgreSQL auto-increments this on every INSERT.
    id: Mapped[int] = mapped_column(primary_key=True)

    # unique=True creates a UNIQUE constraint — no two rows can share an email.
    # index=True creates a B-tree index so lookups by email are fast.
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    name: Mapped[str] = mapped_column(String(255))

    # server_default means PostgreSQL sets this value, not Python.
    # func.now() compiles to NOW() in SQL. This is more reliable than a
    # Python-side default because it uses the database server's clock.
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relationship — not a column, just a Python-side link to Order objects.
    # SQLAlchemy uses this to let you write user.orders and get a list of Order rows.
    orders: Mapped[list["Order"]] = relationship(back_populates="user")
