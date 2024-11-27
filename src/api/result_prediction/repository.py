import datetime
from typing import Tuple

from sqlalchemy import select, desc, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.network.schemas import PredictIn
from src.api.result_prediction.schemas import ResultPredictionPutDto
from src.api.user.schemas import UserOutDto
from src.database.models import ResultPrediction


class ResultPredictionRepository:
    async def create_result_prediction(
            self,
            image_base64: str,
            id_poses: str,
            id_user: int,
            session: AsyncSession
    ):
        new_result_prediction = ResultPrediction(
            id_user=id_user,
            image=image_base64,
            answer=id_poses,
            created_at=datetime.datetime.now()
        )
        session.add(new_result_prediction)
        await session.commit()

    async def get_result_predictions(
            self,
            page: int,
            count: int,
            session: AsyncSession,
            id_user: int | None
    ) -> Tuple[list[ResultPrediction], int]:
        if id_user is not None:
            result_predictions = (await session.execute(
                select(ResultPrediction, func.count().over().label("count"))
                .where(ResultPrediction.id_user == id_user)
                .order_by(desc(ResultPrediction.created_at))
                .offset((page - 1) * count).limit(count)
            )).scalars().all()
            count_predictions = (await session.execute(
                select(func.count(ResultPrediction.id))
                .where(ResultPrediction.id_user == id_user)
            )).scalar()

            return list(result_predictions), count_predictions
        else:
            result_predictions = (await session.execute(
                select(ResultPrediction)
                .order_by(desc(ResultPrediction.created_at))
                .offset((page - 1) * count).limit(count)
            )).scalars().all()
            count_predictions = (await session.execute(
                select(func.count(ResultPrediction.id))
            )).scalar()

            return list(result_predictions), count_predictions

    async def get_result_prediction_by_id(self, id_result_prediction: int, session: AsyncSession) -> ResultPrediction:
        result_prediction = (await session.execute(
            select(ResultPrediction).where(ResultPrediction.id == id_result_prediction)
        )).scalar_one_or_none()
        return result_prediction

    async def put_result_prediction(self, id_result_prediction: int, result_prediction_data: ResultPredictionPutDto, session: AsyncSession):
        await session.execute(
            update(ResultPrediction).where(ResultPrediction.id == id_result_prediction).values(
                is_right=result_prediction_data.is_right,
                right_answer_system=result_prediction_data.right_answer_system,
                right_answer_sanskrit=result_prediction_data.right_answer_sanskrit,
                right_transliteration=result_prediction_data.right_transliteration,
                right_answer_russian=result_prediction_data.right_answer_russian
            )
        )
        await session.commit()
        return await self.get_result_prediction_by_id(id_result_prediction, session)
