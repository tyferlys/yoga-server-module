from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.auth.schemas import Token
from src.api.auth.service import AuthService
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
    response: Response,
    auth_service: AuthService = Depends(AuthService),
    session: AsyncSession = Depends(get_session)
) -> Token:

    result = await auth_service.auth_user(user_data.login, user_data.password, session)
    response.set_cookie(
        key="access_token",
        value=result.access_token,
        httponly=False,  # Защищает cookie от доступа через JavaScript
        secure=False,  # Если у вас нет HTTPS, установите это в False
        samesite="none",
        expires=datetime.now() + timedelta(days=31)
    )
    return result


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