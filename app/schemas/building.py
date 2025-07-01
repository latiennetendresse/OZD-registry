from typing import Optional

from pydantic import BaseModel, Field


class BuildingBase(BaseModel):
    address: str = Field(..., example="г. Москва, ул. Ленина 1, офис 3")
    latitude: float = Field(..., example=55.7558)
    longitude: float = Field(..., example=37.6173)


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BaseModel):
    address: Optional[str] = Field(None, example="г. Москва, ул. Ленина 2")
    latitude: Optional[float] = Field(None, example=55.7560)
    longitude: Optional[float] = Field(None, example=37.6180)


class BuildingOut(BuildingBase):
    id: int

    class Config:
        orm_mode = True
