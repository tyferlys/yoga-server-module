import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from src.api.network.schemas import PredictIn, PredictOut
from src.api.network.utils import send_request_to_network
from src.api.result_prediction.service import ResultPredictionService
from src.api.user.schemas import UserOutDto
from src.api.yoga_pose.service import YogaPoseService


class NetworkService:
    def __init__(self):
        self.yoga_pose_service = YogaPoseService()
        self.result_prediction_service = ResultPredictionService()

    async def prediction(self, prediction_date: PredictIn, user: UserOutDto, cookie_permission: str, session: AsyncSession) -> PredictOut:
        id_poses = await send_request_to_network(prediction_date)
        poses = []
        for id_pose in id_poses:
            poses.append(await self.yoga_pose_service.get_yoga_pose_by_id(id_pose, session))

        if user is not None and user.permission_study:
            await self.result_prediction_service.create_result_prediction(prediction_date, id_poses, user, session)
        elif cookie_permission == "true":
            await self.result_prediction_service.create_result_prediction(prediction_date, id_poses, None, session)

        return PredictOut(yoga_poses=poses)