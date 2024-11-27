from pydantic import BaseModel

from src.database.models import User


class UserAuthDto(BaseModel):
    login: str
    password: str


class UserRegistrationDto(BaseModel):
    login: str
    password: str


class UserOutDto(BaseModel):
    id: int
    login: str
    password: str
    is_admin: bool
    permission_study: bool

    @staticmethod
    def from_user(user: User) -> "UserOutDto":
        return UserOutDto(
            id=user.id,
            login=user.login,
            password=user.password,
            is_admin=user.is_admin,
            permission_study=user.permission_study
        )