from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=True)
    horizon = Column(String, nullable=True)
    link = Column(String, nullable=True)
    countries = Column(String, nullable=True)
    last_updated = Column(String, nullable=True)
    regions = Column(String, nullable=True)
    views = Column(Integer, nullable=True)