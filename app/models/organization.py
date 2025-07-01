from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.session import Base

# таблица many-to-many с activities
organization_activities = Table(
    "organization_activities",
    Base.metadata,
    Column("organization_id", ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", ForeignKey("activities.id"), primary_key=True),
)


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone_numbers = Column(JSONB, nullable=False, default=list)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)

    # many-to-one к Building
    building = relationship(
        "Building",
        back_populates="organizations"
    )

    # many-to-many к Activity
    activities = relationship(
        "Activity",
        secondary=organization_activities,
        back_populates="organizations"
    )

    @property
    def activity_ids(self) -> List[int]:
        """
        Возвращает список ID связанных Activity.
        """
        return [activity.id for activity in self.activities]
