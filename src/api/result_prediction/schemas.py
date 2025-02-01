import json
import math
from datetime import datetime
from typing import Optional, Tuple

from pydantic import BaseModel

from src.api.yoga_pose.schemas import YogaPoseOutDto
from src.database.models import ResultPrediction


class ResultPredictionOutDto(BaseModel):
    id: int
    id_user: int
    image: str
    answer: list[YogaPoseOutDto]
    created_at: datetime

    is_right: Optional[bool]
    right_answer_system: Optional[YogaPoseOutDto]
    right_answer_sanskrit: Optional[str]
    right_transliteration: Optional[str]
    right_answer_russian:  Optional[str]

    @staticmethod
    def from_result_prediction(result_prediction: ResultPrediction, answer: list[YogaPoseOutDto]) -> "ResultPredictionOutDto":
        return ResultPredictionOutDto(
            id=result_prediction.id,
            id_user=result_prediction.id_user,
            image=result_prediction.image,
            answer=answer,
            created_at=result_prediction.created_at,
            is_right=result_prediction.is_right,
            right_answer_system=YogaPoseOutDto.from_yoga_pose(result_prediction.right_answer_system_entity) if result_prediction.right_answer_system_entity is not None else None,
            right_answer_sanskrit=result_prediction.right_answer_sanskrit,
            right_transliteration=result_prediction.right_transliteration,
            right_answer_russian=result_prediction.right_answer_russian
        )


class PaginationResultPredictionOutDto(BaseModel):
    page: int
    all_pages: int
    result_predictions: list[ResultPredictionOutDto]

    @staticmethod
    def from_data(result_predictions: list[Tuple[ResultPrediction, list[YogaPoseOutDto]]], count_predictions: int, count: int, page: int) -> "PaginationResultPredictionOutDto":
        return PaginationResultPredictionOutDto(
            page=page,
            all_pages=math.ceil(count_predictions / count),
            result_predictions=[ResultPredictionOutDto.from_result_prediction(result_prediction[0], result_prediction[1]) for result_prediction in result_predictions]
        )


class ResultPredictionPutDto(BaseModel):
    is_right_top1: Optional[int]
    is_right_top5: Optional[int]
    right_answer_system: Optional[int]
    right_answer_sanskrit: Optional[str]
    right_transliteration: Optional[str]
    right_answer_russian: Optional[str]