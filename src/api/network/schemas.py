from pydantic import BaseModel

from src.api.yoga_pose.schemas import YogaPoseOutDto
from src.database.models import YogaPose


class PredictIn(BaseModel):
    image: str


class PredictOut(BaseModel):
    yoga_poses: list[YogaPoseOutDto]