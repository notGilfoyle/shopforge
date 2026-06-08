from datetime import datetime
from typing import Annotated, Any

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import BeforeValidator

# MongoDB stores IDs as ObjectId (a 12-byte BSON type), but JSON has no such type.
# BeforeValidator(str) converts any ObjectId to a plain string before Pydantic
# validates it, so the API always exposes IDs as strings like "6847a1c2...".
PyObjectId = Annotated[str, BeforeValidator(str)]


class ProductCreate(BaseModel):
    """Fields required to create a new product."""

    name: str
    description: str
    price: float = Field(gt=0, description="Must be positive")
    category: str
    inventory_count: int = Field(default=0, ge=0)

    # This is MongoDB's killer feature for a catalog:
    # every category can store completely different fields here.
    # A book has {"author": ..., "isbn": ...}
    # A TV has  {"screen_size": 55, "resolution": "4K"}
    # No schema changes needed — just put whatever makes sense.
    attributes: dict[str, Any] = {}

    images: list[str] = []


class ProductUpdate(BaseModel):
    """All fields are optional so callers can patch a single field."""

    name: str | None = None
    description: str | None = None
    price: float | None = Field(default=None, gt=0)
    category: str | None = None
    inventory_count: int | None = Field(default=None, ge=0)
    attributes: dict[str, Any] | None = None
    images: list[str] | None = None


class ProductOut(ProductCreate):
    """What the API returns — adds id and timestamps."""

    # validation_alias="_id" tells Pydantic: when *reading* from a MongoDB dict,
    # look for the key "_id". But when *writing* to JSON, use the field name "id".
    #
    # Why not plain alias="_id"?
    # FastAPI serializes models with by_alias=True internally, so alias="_id"
    # would output "_id" in the response — the exact thing we want to hide.
    # validation_alias only affects input; the output always uses the field name.
    id: PyObjectId = Field(validation_alias="_id")

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(populate_by_name=True)
