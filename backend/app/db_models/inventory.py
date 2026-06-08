from sqlalchemy import CheckConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.postgres import Base


class Inventory(Base):
    __tablename__ = "inventory"
    __table_args__ = (CheckConstraint("stock >= 0", name="stock_non_negative"),)

    product_id: Mapped[str] = mapped_column(String(24), primary_key=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
