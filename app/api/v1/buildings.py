from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.building import BuildingRepository
from app.crud.organization import OrganizationRepository
from app.db.session import get_db
from app.models.building import Building
from app.schemas.building import BuildingCreate, BuildingOut, BuildingUpdate
from app.schemas.organization import OrganizationOut

router = APIRouter(
    tags=["buildings"],
)


@router.get("/", response_model=List[BuildingOut])
async def list_buildings(db: AsyncSession = Depends(get_db)):
    repo = BuildingRepository(db)
    return await repo.list()


@router.post("/", response_model=BuildingOut, status_code=status.HTTP_201_CREATED)
async def create_building(
        payload: BuildingCreate,
        db: AsyncSession = Depends(get_db),
):
    repo = BuildingRepository(db)
    building = Building(**payload.dict())
    return await repo.create(building)


@router.get("/{building_id}", response_model=BuildingOut)
async def read_building(
        building_id: int,
        db: AsyncSession = Depends(get_db),
):
    repo = BuildingRepository(db)
    building = await repo.get(building_id)
    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )
    return building


@router.put("/{building_id}", response_model=BuildingOut)
async def update_building(
        building_id: int,
        payload: BuildingUpdate,
        db: AsyncSession = Depends(get_db),
):
    repo = BuildingRepository(db)
    data = payload.dict(exclude_unset=True)
    building = await repo.update(building_id, data)
    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )
    return building


@router.delete("/{building_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_building(
        building_id: int,
        db: AsyncSession = Depends(get_db),
):
    repo = BuildingRepository(db)
    deleted = await repo.delete(building_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )


@router.get("/{building_id}/organizations", response_model=List[OrganizationOut])
async def list_organizations_in_building(
        building_id: int,
        db: AsyncSession = Depends(get_db),
):
    building_repo = BuildingRepository(db)
    if not await building_repo.get(building_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )
    org_repo = OrganizationRepository(db)
    return await org_repo.by_building(building_id)
