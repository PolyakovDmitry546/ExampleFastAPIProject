from typing import Annotated

from pydantic import EmailStr

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, status

from auth.services import AuthGuard

from db import db

from users.models import User
from users.schemas import UserOut, UserUpdate
from users.services import UserService


router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/', response_model=list[UserOut])
async def get_users(session: Annotated[AsyncSession, Depends(db.session_dependency)]):
    user_service = UserService(session)
    users = await user_service.get_users()
    return users


@router.get('/me')
async def read_users_me(
            current_user: Annotated[User, Depends(AuthGuard.get_current_active_user)],
        ):
    return current_user


@router.get('/{id}', response_model=UserOut)
async def get_user_by_id(id: int, session: Annotated[AsyncSession, Depends(db.session_dependency)]):
    user_service = UserService(session)
    user = await user_service.get_user_by_id(id)
    return user


@router.get('/username/{username}', response_model=UserOut)
async def get_user_by_username(username: str, session: Annotated[AsyncSession, Depends(db.session_dependency)]):
    user_service = UserService(session)
    user = await user_service.get_user_by_username(username)
    return user


@router.get('/email/{email}', response_model=UserOut)
async def get_user_by_email(email: EmailStr, session: Annotated[AsyncSession, Depends(db.session_dependency)]):
    user_service = UserService(session)
    user = await user_service.get_user_by_email(email)
    return user


@router.patch('/{id}', response_model=UserOut)
async def path_user(id: int, update_data: UserUpdate, session: Annotated[AsyncSession, Depends(db.session_dependency)]):
    user_service = UserService(session)
    user = await user_service.update_user(id, update_data)
    return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, session: Annotated[AsyncSession, Depends(db.session_dependency)]):
    user_service = UserService(session)
    await user_service.delete_user(id)
