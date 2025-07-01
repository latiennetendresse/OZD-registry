from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base
from app.models.organization import organization_activities


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True)

    parent = relationship(
        "Activity",
        back_populates="children",
        remote_side=[id]
    )

    children = relationship(
        "Activity",
        back_populates="parent",
        cascade="all, delete-orphan"
    )

    organizations = relationship(
        "Organization",
        secondary=organization_activities,
        back_populates="activities"
    )
