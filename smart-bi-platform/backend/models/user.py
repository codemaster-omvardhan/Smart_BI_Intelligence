from sqlalchemy import Column, Integer, String, ForeignKey
from db.base import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True)

    password = Column(String)

    organization_id = Column(Integer, ForeignKey("organizations.id"))