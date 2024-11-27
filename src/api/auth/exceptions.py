from fastapi import HTTPException
from starlette import status


class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(status.HTTP_401_UNAUTHORIZED, "Ошибка в данных для авторизации")


class LoginExistsException(HTTPException):
    def __init__(self):
        super().__init__(status.HTTP_409_CONFLICT, "Пользователь с таким логином уже существует")