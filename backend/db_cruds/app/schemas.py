from pydantic import BaseModel
from typing import Optional

class DatasetBase(BaseModel):
    name: str
    type: Optional[str] = None
    horizon: Optional[str] = None
    link: Optional[str] = None
    countries: Optional[str] = None
    last_updated: Optional[str] = None
    regions: Optional[str] = None
    views: Optional[int] = None

class DatasetCreate(DatasetBase):
    pass

class DatasetUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    horizon: Optional[str] = None
    link: Optional[str] = None
    countries: Optional[str] = None
    last_updated: Optional[str] = None
    regions: Optional[str] = None
    views: Optional[int] = None

class DatasetResponse(DatasetBase):
    id: int
    
    class Config:
        orm_mode = True
        from_attributes = True