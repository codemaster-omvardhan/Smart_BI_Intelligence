from sqlalchemy import Column, Integer, String, ForeignKey
from db.base import Base

class DatasetMetadata(Base):

    __tablename__ = "dataset_metadata"

    id = Column(Integer, primary_key=True, index=True)

    dataset_id = Column(Integer, ForeignKey("datasets.id"))

    numeric_columns = Column(String)

    date_column = Column(String)

    detected_metrics = Column(String)