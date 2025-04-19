from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api.request_to_admin_status.schemas import RequestToAdminStatusEnum
from src.database.models import RequestToAdminStatus


class RequestToAdminStatusRepository:
    async def create_request_to_admin_status(self, user_id: int, session: AsyncSession) -> RequestToAdminStatus:
        request_to_admin_status = RequestToAdminStatus(
            id_user=user_id,
            status=RequestToAdminStatusEnum.waiting.value,
        )
        session.add(request_to_admin_status)
        await session.commit()
        await session.flush()
        return request_to_admin_status

    async def get_request_to_admin_status_by_id(self, id_record: int, session: AsyncSession) -> RequestToAdminStatus:
        request_to_admin_status = (await session.execute(
            select(RequestToAdminStatus).options(selectinload(RequestToAdminStatus.user)).where(RequestToAdminStatus.id == id_record)
        )).scalar_one_or_none()
        return request_to_admin_status