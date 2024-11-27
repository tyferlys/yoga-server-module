from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user.schemas import UserRegistrationDto
from src.database.models import User


class UserRepository:
    async def get_user_by_login(self, login: str, session: AsyncSession) -> User | None:
        user = await session.execute(
            select(User).where(User.login == login)
        )
        return user.scalar_one_or_none()

    async def create_user(self, user_data: UserRegistrationDto, session: AsyncSession) -> User:
        user: User = User(
            login=user_data.login,
            password=user_data.password,
            is_admin=False,
            permission_study=False
        )
        session.add(user)
        await session.commit()
        await session.flush()
        return user

    async def patch_permission_study_by_id(self, id: int, permission: bool, session: AsyncSession) -> User:
        user = await session.execute(
            select(User).where(User.id == id)
        )
        user = user.scalar_one_or_none()
        user.permission_study = permission
        await session.commit()
        await session.flush()
        return user