from typing import List, Optional

from pydantic import BaseModel, Field


class OrganizationBase(BaseModel):
    name: str = Field(..., example="ООО “Рога и Копыта”")
    phone_numbers: List[str] = Field(..., example=["2-222-222", "3-333-333"])
    building_id: int = Field(..., example=1)
    activity_ids: List[int] = Field(..., example=[1, 2])


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    phone_numbers: Optional[List[str]] = None
    building_id: Optional[int] = None
    activity_ids: Optional[List[int]] = None


class OrganizationOut(BaseModel):
    id: int
    name: str
    phone_numbers: List[str]
    building_id: int
    activity_ids: List[int]

    class Config:
        orm_mode = True
