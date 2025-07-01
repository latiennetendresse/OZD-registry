from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.activity import Activity
from app.services.tree import ActivityTreeService


class ActivityRepository:
    """
    Репозиторий для работы с сущностью Activity.
    """

    def __init__(self, session: AsyncSession):
        self._session = session

    async def list(self) -> List[Activity]:
        stmt = select(Activity).options(
            selectinload(Activity.children)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get(self, activity_id: int) -> Optional[Activity]:
        stmt = (
            select(Activity)
            .where(Activity.id == activity_id)
            .options(selectinload(Activity.children))
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, activity: Activity) -> Activity:
        self._session.add(activity)
        await self._session.commit()
        await self._session.refresh(activity)
        return activity

    async def update(self, activity_id: int, data: dict) -> Optional[Activity]:
        activity = await self.get(activity_id)
        if not activity:
            return None
        for field, val in data.items():
            setattr(activity, field, val)
        self._session.add(activity)
        await self._session.commit()
        await self._session.refresh(activity)
        return activity

    async def delete(self, activity_id: int) -> bool:
        activity = await self.get(activity_id)
        if not activity:
            return False
        await self._session.delete(activity)
        await self._session.commit()
        return True

    async def descendant_ids(self, root_id: int, max_level: int = 3) -> List[int]:
        """
        Собирает ID корня и всех его потомков до указанной глубины,
        с помощью ActivityTreeService.
        """
        all_acts = await self.list()
        tree = ActivityTreeService(all_acts)
        return tree.gather_descendant_ids(root_id, max_level)
