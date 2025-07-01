from typing import List, Optional

from pydantic import BaseModel, Field


class ActivityBase(BaseModel):
    name: str = Field(..., example="Молочная продукция")
    parent_id: Optional[int] = Field(None, example=1)


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Обновлённое название")
    parent_id: Optional[int] = Field(None, example=2)


class ActivityOut(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]

    class Config:
        orm_mode = True
