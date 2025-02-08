from sqlalchemy.ext.asyncio import AsyncSession

from src.api.yoga_pose.repository import YogaPoseRepository
from src.api.yoga_pose.schemas import YogaPoseOutDto, PaginationYogaPoseOutDto, YogaPosePutDto


class YogaPoseService:
    def __init__(self):
        self.yoga_pose_repository = YogaPoseRepository()


    async def get_yoga_poses(self, page: int, count: int, text: str, session: AsyncSession) -> PaginationYogaPoseOutDto:
        yoga_poses, count_pose = await self.yoga_pose_repository.get_yoga_poses(page, count, text, session)
        return PaginationYogaPoseOutDto.from_data(yoga_poses, count_pose, count, page)

    async def get_yoga_pose_by_id(self, id_yoga_pose: int, session: AsyncSession) -> YogaPoseOutDto:
        yoga_pose = await self.yoga_pose_repository.get_yoga_pose_by_id(id_yoga_pose, session)
        return YogaPoseOutDto.from_yoga_pose(yoga_pose)

    async def get_yoga_pose_by_ids(self, ids_yoga_pose: list[int], session: AsyncSession) -> list[YogaPoseOutDto]:
        yoga_poses = await self.yoga_pose_repository.get_yoga_pose_by_ids(ids_yoga_pose, session)
        return [YogaPoseOutDto.from_yoga_pose(yoga_pose) for yoga_pose in yoga_poses]

    async def put_yoga_pose_by_id(self, id_yoga_pose: int, yoga_pose_data: YogaPosePutDto, session: AsyncSession) -> YogaPoseOutDto:
        yoga_pose = await self.yoga_pose_repository.put_yoga_pose_by_id(id_yoga_pose, yoga_pose_data, session)
        return YogaPoseOutDto.from_yoga_pose(yoga_pose)