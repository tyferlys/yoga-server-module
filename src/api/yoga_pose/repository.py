from typing import Union, Tuple

from sqlalchemy import select, func, update, asc, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing import in_

from src.api.yoga_pose.schemas import YogaPosePutDto
from src.database.models import YogaPose


class YogaPoseRepository:
    async def get_yoga_poses(self, page: int, count: int, text: str, session: AsyncSession) -> Tuple[list[YogaPose], int]:
        if text == "":
            yoga_poses = (await session.execute(
                select(YogaPose).order_by(asc(YogaPose.id)).offset((page - 1) * count).limit(count)
            )).scalars().all()
            count_poses = (await session.execute(
                select(func.count(YogaPose.id))
            )).scalar()
        else:
            yoga_poses = (await session.execute(
                select(YogaPose).where(or_(
                    YogaPose.title_russian.ilike(f"%{text}%"),
                    YogaPose.title_sanskrit.ilike(f"%{text}%"),
                    YogaPose.title_sanskrit.ilike(f"%{text}%")
                )).order_by(asc(YogaPose.id)).offset((page - 1) * count).limit(count)
            )).scalars().all()
            count_poses = (await session.execute(
                select(func.count(YogaPose.id)).where(or_(
                    YogaPose.title_russian.ilike(f"%{text}%"),
                    YogaPose.title_sanskrit.ilike(f"%{text}%"),
                    YogaPose.title_sanskrit.ilike(f"%{text}%")
                ))
            )).scalar()

        return list(yoga_poses), count_poses

    async def get_yoga_pose_by_id(self, id_yoga_pose: int, session: AsyncSession) -> YogaPose:
        yoga_pose = await session.execute(
            select(YogaPose).where(YogaPose.id == id_yoga_pose)
        )
        return yoga_pose.scalar_one_or_none()

    async def get_yoga_pose_by_ids(self, ids_yoga_pose: list[int], session: AsyncSession) -> list[YogaPose]:
        yoga_poses = await session.execute(
            select(YogaPose).where(YogaPose.id.in_(ids_yoga_pose))
        )
        return list(yoga_poses.scalars().all())

    async def put_yoga_pose_by_id(self, id_yoga_pose: int, yoga_pose_data: YogaPosePutDto, session: AsyncSession) -> YogaPose:
        await session.execute(
            update(YogaPose).where(YogaPose.id == id_yoga_pose).values(
                title_sanskrit=yoga_pose_data.title_sanskrit,
                title_transliteration=yoga_pose_data.title_transliteration,
                title_russian=yoga_pose_data.title_russian
            )
        )
        await session.commit()
        return await self.get_yoga_pose_by_id(id_yoga_pose, session)