from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.repository import UserRepository
from src.api.user.schemas import UserOutDto, UserRegistrationDto
from src.database.models import User


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    async def get_user_by_login(self, login: str, session: AsyncSession) -> UserOutDto | None:
        user: User = await self.user_repository.get_user_by_login(login, session)
        return UserOutDto.from_user(user) if user is not None else None

    async def create_user(self, user_data: UserRegistrationDto, session: AsyncSession) -> UserOutDto | None:
        user: User = await self.user_repository.create_user(user_data, session)
        return UserOutDto.from_user(user) if user is not None else None

    async def patch_permission_study(self, user: UserOutDto, permission: bool, session: AsyncSession) -> UserOutDto:
        user: User = await self.user_repository.patch_permission_study_by_id(user.id, permission, session)
        return UserOutDto.from_user(user)

    async def verify_user(self, mail: str, session: AsyncSession):
        user: User = await self.user_repository.verify_user(mail, session)
        return UserOutDto.from_user(user)

