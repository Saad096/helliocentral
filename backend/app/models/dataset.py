from pydantic import BaseModel

class Dataset(BaseModel):
    file_id: str
    name: str
    size: int
    format: str