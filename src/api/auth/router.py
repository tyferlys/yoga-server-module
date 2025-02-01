from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.api.auth.exceptions import CredentialsException
from src.api.auth.schemas import Token
from src.api.auth.service import AuthService
from src.api.auth.utils import authenticate_user, create_access_token
from src.api.user.schemas import UserOutDto, UserAuthDto, UserRegistrationDto
from src.database.config import get_session

router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends(AuthService),
    session: AsyncSession = Depends(get_session)
) -> Token:
    return await auth_service.auth_user(form_data.username, form_data.password, session)


@router.post("")
async def auth(
    user_data: UserAuthDto,
    auth_service: AuthService = Depends(AuthService),
    session: AsyncSession = Depends(get_session)
) -> Token:
    return await auth_service.auth_user(user_data.login, user_data.password, session)


@router.get("/verify/{token}")
async def verify_mail(
    token: str,
    auth_service: AuthService = Depends(AuthService),
    session: AsyncSession = Depends(get_session)
) -> UserOutDto:
    return await auth_service.verify_token(token, session)

@router.post("/registration")
async def registration(
    user_data: UserRegistrationDto,
    auth_service: AuthService = Depends(AuthService),
    session: AsyncSession = Depends(get_session)
) -> UserOutDto:
    return await auth_service.registration_user(user_data, session)