from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse

from src.api.auth.schemas import Token, ResetPasswordDto
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
        expires=60 * 60 * 24 * 31,
        max_age=60 * 60 * 24 * 31,
        path='/',
    )
    return result


@router.get("/verify/{token}", response_class=HTMLResponse)
async def verify_mail(
    token: str,
    auth_service: AuthService = Depends(AuthService),
    session: AsyncSession = Depends(get_session)
):
    _ = await auth_service.verify_token(token, session)
    return """
        <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <title>Подтверждение аккаунта</title>
                <style>
                    body {
                        background-color: #f4f6f8;
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                    }
                    .message-box {
                        background-color: #ffffff;
                        padding: 40px 60px;
                        border-radius: 12px;
                        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                        text-align: center;
                    }
                    .message-box h1 {
                        font-size: 24px;
                        margin: 0;
                    }
                </style>
            </head>
            <body>
                <div class="message-box">
                    <h1>Аккаунт был успешно подтвержден</h1>
                </div>
            </body>
        </html>
    """

@router.post("/registration")
async def registration(
    user_data: UserRegistrationDto,
    auth_service: AuthService = Depends(AuthService),
    session: AsyncSession = Depends(get_session)
) -> UserOutDto:
    return await auth_service.registration_user(user_data, session)

@router.get("/reset_password_request")
async def reset_password_request(
    login: str,
    auth_service: AuthService = Depends(AuthService),
    session: AsyncSession = Depends(get_session)
) -> None:
    return await auth_service.reset_password_request(login, session)


@router.patch("/reset_password")
async def reset_password(
    reset_password_data: ResetPasswordDto,
    auth_service: AuthService = Depends(AuthService),
    session: AsyncSession = Depends(get_session)
) -> UserOutDto:
    return await auth_service.reset_password(reset_password_data, session)