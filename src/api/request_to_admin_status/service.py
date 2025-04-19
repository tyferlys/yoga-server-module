from sqlalchemy.ext.asyncio import AsyncSession

from src.api.request_to_admin_status.repository import RequestToAdminStatusRepository
from src.api.request_to_admin_status.schemas import RequestToAdminStatusOutDto
from src.api.user.schemas import UserOutDto


class RequestToAdminStatusService:
    def __init__(self):
        self.request_to_admin_status_repository = RequestToAdminStatusRepository()

    async def create_request_to_admin_status(self, user: UserOutDto, session: AsyncSession) -> RequestToAdminStatusOutDto:
        request_to_admin_status = await self.request_to_admin_status_repository.create_request_to_admin_status(user.id, session)
        request_to_admin_status_full  = await self.request_to_admin_status_repository.get_request_to_admin_status_by_id(request_to_admin_status.id, session)
        return RequestToAdminStatusOutDto.from_request_to_admin_status(request_to_admin_status_full)