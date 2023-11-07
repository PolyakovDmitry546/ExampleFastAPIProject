from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status

from jose import JWTError, jwt

from sqlalchemy.ext.asyncio import AsyncSession

from settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

from auth import oauth2_scheme
from auth.exceptions import WrongPasswordError, WrongUsernameError
from auth.schemas import AuthScheme, SignUpScheme, TokenDataScheme
from auth.utils import create_access_token, verify_password

from db import db

from users.models import User
from users.schemas import UserCreate
from users.services import UserService


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def signup(self, user_data: SignUpScheme):
        user_service = UserService(self.session)
        user = await user_service.create_user(UserCreate(**user_data.model_dump()))
        return user

    async def authenticate(self, user_data: AuthScheme) -> str:
        user_service = UserService(self.session)
        user = await user_service.get_user_by_username(user_data.username)
        if user is None:
            raise WrongUsernameError()
        if not verify_password(user_data.password, user.password):
            raise WrongPasswordError()

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": f'{user.id}'}, expires_delta=access_token_expires)
        return access_token


class AuthGuard:
    @staticmethod
    async def get_current_user(
                token: Annotated[str, Depends(oauth2_scheme)],
                session: Annotated[AsyncSession, Depends(db.session_dependency)],
            ) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            id = int(payload.get("sub"))
            if id is None:
                raise credentials_exception
            token_data = TokenDataScheme(id=id)
        except JWTError:
            raise credentials_exception
        user_service = UserService(session)
        user = await user_service.get_user_by_id(token_data.id)
        if user is None:
            raise credentials_exception
        return user

    @staticmethod
    async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
        current_user = await current_user
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
