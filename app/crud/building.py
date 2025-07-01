from typing import List, Optional

from app.models.building import Building
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BuildingRepository:
    """
    Репозиторий для работы с сущностью Building.
    """

    def __init__(self, session: AsyncSession):
        self._session = session

    async def list(self) -> List[Building]:
        result = await self._session.execute(select(Building))
        return result.scalars().all()

    async def get(self, building_id: int) -> Optional[Building]:
        result = await self._session.execute(
            select(Building).where(Building.id == building_id)
        )
        return result.scalar_one_or_none()

    async def create(self, building: Building) -> Building:
        self._session.add(building)
        await self._session.commit()
        await self._session.refresh(building)
        return building

    async def update(self, building_id: int, data: dict) -> Optional[Building]:
        building = await self.get(building_id)
        if not building:
            return None
        for field, val in data.items():
            setattr(building, field, val)
        self._session.add(building)
        await self._session.commit()
        await self._session.refresh(building)
        return building

    async def delete(self, building_id: int) -> bool:
        building = await self.get(building_id)
        if not building:
            return False
        await self._session.delete(building)
        await self._session.commit()
        return True
