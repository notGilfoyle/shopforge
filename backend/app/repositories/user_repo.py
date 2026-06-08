from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_models.user import User
from app.models.user import UserCreate, UserOut


async def create(db: AsyncSession, data: UserCreate) -> UserOut:
    user = User(email=data.email, name=data.name)
    db.add(user)
    await db.commit()
    # refresh loads the server-generated values (id, created_at) back into the object
    await db.refresh(user)
    return UserOut.model_validate(user)


async def get_by_id(db: AsyncSession, user_id: int) -> UserOut | None:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        return None
    return UserOut.model_validate(user)


async def get_by_email(db: AsyncSession, email: str) -> UserOut | None:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        return None
    return UserOut.model_validate(user)
