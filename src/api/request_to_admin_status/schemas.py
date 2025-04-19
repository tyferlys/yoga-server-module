from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from src.api.user.schemas import UserOutDto
from src.database.models import RequestToAdminStatus


class RequestToAdminStatusEnum(Enum):
    waiting: str = "В ожидании"
    rejected: str = "Отклонена"
    accept: str = "Принята"


class RequestToAdminStatusOutDto(BaseModel):
    id: int
    user: UserOutDto
    status: str
    created_at: str

    @classmethod
    def from_request_to_admin_status(cls, request_to_admin_status: RequestToAdminStatus) -> "RequestToAdminStatusDto":
        return RequestToAdminStatusOutDto(
            id=request_to_admin_status.id,
            user=UserOutDto.from_user(request_to_admin_status.user),
            status=request_to_admin_status.status,
            created_at=str(request_to_admin_status.created_at)
        )