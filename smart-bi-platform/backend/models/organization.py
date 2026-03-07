from sqlalchemy import Column, Integer, String, DateTime
from db.base import Base
from datetime import datetime


class Organization(Base):

    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)