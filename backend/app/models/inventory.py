from pydantic import BaseModel, ConfigDict, Field


class InventoryOut(BaseModel):
    product_id: str
    stock: int
    model_config = ConfigDict(from_attributes=True)


class InventorySet(BaseModel):
    stock: int = Field(ge=0)
