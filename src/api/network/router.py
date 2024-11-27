from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.utils import get_current_user, get_current_user_soft
from src.api.network.schemas import PredictIn, PredictOut
from src.api.network.service import NetworkService
from src.api.user.schemas import UserOutDto
from src.database.config import get_session

router = APIRouter()


@router.post("/prediction")
async def prediction(
    prediction_date: PredictIn,
    request: Request,
    network_service: NetworkService = Depends(NetworkService),
    session: AsyncSession = Depends(get_session),
    user: UserOutDto = Depends(get_current_user_soft)
) -> PredictOut:
    cookie_permission = request.cookies.get("permission_study")
    return await network_service.prediction(prediction_date, user, cookie_permission, session)