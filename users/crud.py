from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from users.models import User
from users.schemas import UserCreate, UserUpdate
from auth.utils import get_password_hash


async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user_by_id(session: AsyncSession, id: int) -> User | None:
    return await session.get(User, id)


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).filter(User.username == username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    stmt = select(User).filter(User.email == email)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user


async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
    hashed_password = get_password_hash(user_data.password)
    user = User(**user_data.model_dump())
    user.password = hashed_password
    session.add(user)
    await session.commit()
    return user


async def update_user(session: AsyncSession, user: User, update_data: UserUpdate) -> User:
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    await session.commit()
    return user


async def delete_user(session: AsyncSession, user: User) -> None:
    await session.delete(user)
    await session.commit()
