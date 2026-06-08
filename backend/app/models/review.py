from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class ReviewCreate(BaseModel):
    user_id: int
    rating: int = Field(ge=1, le=5)
    title: str = Field(max_length=200)
    body: str


class ReviewOut(ReviewCreate):
    id: PyObjectId = Field(validation_alias="_id")
    product_id: str
    created_at: datetime
    model_config = ConfigDict(populate_by_name=True)
