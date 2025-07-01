from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.activity import ActivityRepository
from app.crud.organization import OrganizationRepository
from app.db.session import get_db
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityOut, ActivityUpdate
from app.schemas.organization import OrganizationOut

router = APIRouter(tags=["activities"])


@router.get("/", response_model=List[ActivityOut])
async def list_activities(db: AsyncSession = Depends(get_db)):
    repo = ActivityRepository(db)
    return await repo.list()


@router.post("/", response_model=ActivityOut, status_code=201)
async def create_activity(
        activity_in: ActivityCreate,
        db: AsyncSession = Depends(get_db),
):
    repo = ActivityRepository(db)

    act = Activity(name=activity_in.name, parent_id=activity_in.parent_id)
    created = await repo.create(act)

    loaded = await repo.get(created.id)
    if not loaded:
        raise HTTPException(500, "Failed to load created Activity")
    return loaded


@router.get("/{activity_id}", response_model=ActivityOut)
async def read_activity(activity_id: int, db: AsyncSession = Depends(get_db)):
    repo = ActivityRepository(db)
    act = await repo.get(activity_id)
    if not act:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Activity not found")
    return act


@router.put("/{activity_id}", response_model=ActivityOut)
async def update_activity(
        activity_id: int,
        activity: ActivityUpdate,
        db: AsyncSession = Depends(get_db),
):
    repo = ActivityRepository(db)
    data = activity.dict(exclude_unset=True)
    act = await repo.update(activity_id, data)
    if not act:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Activity not found")
    return act


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(activity_id: int,
                          db: AsyncSession = Depends(get_db)):
    repo = ActivityRepository(db)
    deleted = await repo.delete(activity_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Activity not found")


@router.get("/{root_id}/organizations", response_model=List[OrganizationOut])
async def list_orgs_by_activity(
        root_id: int,
        level: int = Query(3, ge=1, le=3),
        db: AsyncSession = Depends(get_db),
):
    org_repo = OrganizationRepository(db)
    return await org_repo.by_activity(root_id, level)
