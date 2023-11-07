from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from auth.exceptions import WrongPasswordError, WrongUsernameError
from auth.schemas import AuthScheme, SignUpScheme, TokenScheme
from auth.services import AuthService

from db import db

from users.schemas import UserOut


router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/signup', response_model=UserOut)
async def signup(data: SignUpScheme, session: Annotated[AsyncSession, Depends(db.session_dependency)]):
    auth_service = AuthService(session)
    user = await auth_service.signup(data)
    return user


@router.post("/login", response_model=TokenScheme)
async def login_for_access_token(
            form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
            session: Annotated[AsyncSession, Depends(db.session_dependency)],
        ):
    user_data = AuthScheme(username=form_data.username, password=form_data.password)
    auth_service = AuthService(session)
    try:
        access_token = await auth_service.authenticate(user_data)
    except WrongPasswordError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except WrongUsernameError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"access_token": access_token, "token_type": "bearer"}
