from typing import List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.activity import Activity
from app.models.organization import Organization
from app.services.geosearch import GeoSearchService
from app.services.tree import ActivityTreeService


class OrganizationRepository:
    """
    Репозиторий для работы с сущностью Organization.
    """

    def __init__(self, session: AsyncSession):
        self._session = session
        self._geo = GeoSearchService()
        self._tree_cls = ActivityTreeService

    async def list(self) -> List[Organization]:
        stmt = (
            select(Organization)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities).selectinload(Activity.children),
            )
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get(self, org_id: int) -> Optional[Organization]:
        stmt = (
            select(Organization)
            .where(Organization.id == org_id)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities).selectinload(Activity.children),
            )
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, org: Organization) -> Organization:
        self._session.add(org)
        await self._session.commit()
        await self._session.refresh(org)
        return org

    async def update(self, org_id: int, data: dict) -> Optional[Organization]:
        org = await self.get(org_id)
        if not org:
            return None
        if "activity_ids" in data:
            ids = data.pop("activity_ids")
            org.activities = [Activity(id=i) for i in ids]
        for field, val in data.items():
            setattr(org, field, val)
        self._session.add(org)
        await self._session.commit()
        await self._session.refresh(org)
        return org

    async def delete(self, org_id: int) -> bool:
        org = await self.get(org_id)
        if not org:
            return False
        await self._session.delete(org)
        await self._session.commit()
        return True

    async def by_building(self, building_id: int) -> List[Organization]:
        stmt = (
            select(Organization)
            .where(Organization.building_id == building_id)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities).selectinload(Activity.children),
            )
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def by_activity(
            self,
            root_activity_id: int,
            max_level: int = 3
    ) -> List[Organization]:

        stmt_acts = select(Activity).options(
            selectinload(Activity.children)
            .selectinload(Activity.children)
        )
        all_acts = (await self._session.execute(stmt_acts)).scalars().all()

        tree = self._tree_cls(all_acts)
        ids = tree.gather_descendant_ids(root_activity_id, max_level)
        if not ids:
            return []

        stmt = (
            select(Organization)
            .distinct(Organization.id)
            .join(Organization.activities)
            .where(Activity.id.in_(ids))
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities)
            )
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def in_radius(self, center: Tuple[float, float], radius_km: float) -> List[Organization]:
        orgs = await self.list()
        return self._geo.filter_by_radius(orgs, center, radius_km)

    async def in_bbox(self, sw: Tuple[float, float], ne: Tuple[float, float]) -> List[Organization]:
        orgs = await self.list()
        return self._geo.filter_by_bbox(orgs, sw, ne)

    async def search_by_name(self, name_substr: str) -> List[Organization]:
        stmt = (
            select(Organization)
            .where(Organization.name.ilike(f"%{name_substr}%"))
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities).selectinload(Activity.children),
            )
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
