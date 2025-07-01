from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.organization import OrganizationRepository
from app.db.session import get_db
from app.models.activity import Activity
from app.models.organization import Organization
from app.schemas.organization import (OrganizationCreate, OrganizationOut,
                                      OrganizationUpdate)

router = APIRouter(tags=["organizations"])


@router.get("/", response_model=List[OrganizationOut])
async def list_organizations(
        name: Optional[str] = Query(None, description="Поиск по части названия"),
        lat: Optional[float] = Query(None, description="Центр поиска (широта)"),
        lon: Optional[float] = Query(None, description="Центр поиска (долгота)"),
        radius: Optional[float] = Query(None, description="Радиус в км"),
        sw_lat: Optional[float] = Query(None, description="Юго-западная широта"),
        sw_lon: Optional[float] = Query(None, description="Юго-западная долгота"),
        ne_lat: Optional[float] = Query(None, description="Северо-восточная широта"),
        ne_lon: Optional[float] = Query(None, description="Северо-восточная долгота"),
        db: AsyncSession = Depends(get_db),
):
    repo = OrganizationRepository(db)

    if name:
        return await repo.search_by_name(name)

    if lat is not None and lon is not None and radius is not None:
        return await repo.in_radius((lat, lon), radius)

    if sw_lat is not None and sw_lon is not None and ne_lat is not None and ne_lon is not None:
        return await repo.in_bbox((sw_lat, sw_lon), (ne_lat, ne_lon))

    return await repo.list()


@router.post("/", response_model=OrganizationOut, status_code=201)
async def create_organization(
        organization_in: OrganizationCreate,
        db: AsyncSession = Depends(get_db),
):
    repo = OrganizationRepository(db)

    acts = []
    for act_id in organization_in.activity_ids:
        act = await db.get(Activity, act_id)
        if act is None:
            raise HTTPException(status_code=404,
                                detail=f"Activity {act_id} not found")
        acts.append(act)

    org = Organization(
        name=organization_in.name,
        phone_numbers=organization_in.phone_numbers,
        building_id=organization_in.building_id,
        activities=acts,
    )

    created = await repo.create(org)
    return await repo.get(created.id)


@router.get("/{org_id}", response_model=OrganizationOut)
async def read_organization(org_id: int, db: AsyncSession = Depends(get_db)):
    repo = OrganizationRepository(db)
    org = await repo.get(org_id)
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Organization not found")
    return org


@router.put("/{org_id}", response_model=OrganizationOut)
async def update_organization(
        org_id: int,
        organization_in: OrganizationUpdate,
        db: AsyncSession = Depends(get_db),
):
    repo = OrganizationRepository(db)
    data = organization_in.dict(exclude_unset=True)

    if "activity_ids" in data:
        from app.models.activity import Activity
        acts = []
        for act_id in data.pop("activity_ids"):
            act = await db.get(Activity, act_id)
            if act is None:
                raise HTTPException(status_code=404,
                                    detail=f"Activity {act_id} not found")
            acts.append(act)
        data["activities"] = acts

    updated = await repo.update(org_id, data)
    if not updated:
        raise HTTPException(status_code=404,
                            detail="Organization not found")
    return await repo.get(org_id)


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(org_id: int, db: AsyncSession = Depends(get_db)):
    repo = OrganizationRepository(db)
    deleted = await repo.delete(org_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Organization not found")
