from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Обратная сторона отношения к Organization
    organizations = relationship(
        "Organization",
        back_populates="building",
        cascade="all, delete-orphan"
    )
