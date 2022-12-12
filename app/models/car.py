from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean, TIMESTAMP, func,
)

from app.database.connect import Base


class Car(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(63), nullable=False)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP, default=func.now())
