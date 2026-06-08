from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class OrderItemIn(BaseModel):
    """One line of a new order — a product and how many the customer wants."""
    product_id: str = Field(description="MongoDB ObjectId of the product")
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    user_id: int
    items: list[OrderItemIn] = Field(min_length=1, description="At least one item required")


class OrderItemOut(BaseModel):
    id: int
    product_id: str
    product_name: str    # denormalized copy from MongoDB at order time
    quantity: int
    unit_price: Decimal
    subtotal: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrderOut(BaseModel):
    id: int
    user_id: int
    status: str
    total_amount: Decimal
    items: list[OrderItemOut]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
