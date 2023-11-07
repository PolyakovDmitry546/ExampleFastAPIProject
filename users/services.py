from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from users import crud
from users.models import User
from users.schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_users(self) -> list[User]:
        users = await crud.get_users(self.session)
        return users

    async def get_user_by_id(self, id: int) -> User:
        user = await crud.get_user_by_id(self.session, id)
        if user is None:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'User with id {id} not found',
                )
        return user

    async def get_user_by_username(self, username: str) -> User:
        user = await crud.get_user_by_username(self.session, username)
        if user is None:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'User with username {username} not found',
                )
        return user

    async def get_user_by_email(self, email: str) -> User:
        user = await crud.get_user_by_email(self.session, email)
        if user is None:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'User with email {email} not found',
                )
        return user

    async def create_user(self, user_data: UserCreate):
        try:
            user = await crud.create_user(self.session, user_data)
            return user
        except IntegrityError as e:
            error_message = e.args[0]
            if 'UNIQUE constraint failed' in error_message:
                detail = 'Incorrect request'
                if 'username' in error_message:
                    detail = f'Username "{user_data.username}" is already use'
                if 'email' in error_message:
                    detail = f'Email "{user_data.email}" is already use'
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=detail,
                )
            else:
                raise e

    async def update_user(self, id: int, update_data: UserUpdate) -> User:
        user = await self.get_user_by_id(id)
        try:
            user = await crud.update_user(self.session, user, update_data)
        except IntegrityError as e:
            error_message = e.args[0]
            if 'UNIQUE constraint failed' in error_message:
                detail = 'Incorrect request'
                if 'username' in error_message:
                    detail = f'Username "{update_data.username}" is already use'
                if 'email' in error_message:
                    detail = f'Email "{update_data.email}" is already use'
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=detail,
                )
            else:
                raise e
        return user

    async def delete_user(self, id: int) -> None:
        user = await self.get_user_by_id(id)
        await crud.delete_user(self.session, user)
