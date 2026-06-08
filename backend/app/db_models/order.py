"""
SQLAlchemy ORM models for orders and order_items.

Two tables, one relationship:
  orders      — one row per purchase, linked to a user
  order_items — one row per product line within an order (the join table)

The product_id column stores a MongoDB ObjectId as a plain string.
There is intentionally no foreign key to MongoDB — relational databases
can only enforce FK constraints within the same database engine.
Referential integrity across Postgres ↔ MongoDB is the app's responsibility.
"""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.postgres import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    # ForeignKey("users.id") creates the FK constraint in PostgreSQL.
    # If you try to insert an order with a user_id that doesn't exist in
    # users.id, PostgreSQL will reject it with a constraint violation.
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    # Simple string status. An Enum column would also work, but strings
    # are easier to extend without a migration.
    status: Mapped[str] = mapped_column(String(50), default="pending")

    # Numeric(10, 2) → up to 10 digits, 2 after the decimal point.
    # Always use Numeric (not Float) for money — floats have rounding errors.
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # back_populates wires up the two sides of the relationship.
    user: Mapped["User"] = relationship(back_populates="orders")

    # cascade="all, delete-orphan" means: if you delete an Order,
    # SQLAlchemy automatically deletes all its OrderItems too.
    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), index=True)

    # MongoDB ObjectId — 24 hex characters. No FK constraint possible
    # across database engines, so we document the intent with a comment.
    product_id: Mapped[str] = mapped_column(String(24))

    # Denormalized: we copy the product name at order time.
    # If the product name changes in MongoDB later, the order history
    # still shows what the customer actually bought.
    product_name: Mapped[str] = mapped_column(String(255))

    quantity: Mapped[int] = mapped_column(Integer)

    # Snapshot the price at purchase time — products can change price later.
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    subtotal: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    order: Mapped["Order"] = relationship(back_populates="items")
