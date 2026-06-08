from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    # EmailStr validates format — rejects "notanemail", accepts "user@example.com"
    email: EmailStr
    name: str


class UserOut(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime

    # from_attributes=True (formerly orm_mode) lets Pydantic read values
    # from SQLAlchemy ORM objects (attributes) instead of only dicts.
    model_config = ConfigDict(from_attributes=True)
