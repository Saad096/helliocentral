from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.models import Base
from app.schemas import DatasetCreate, DatasetUpdate, DatasetResponse
from app.database import engine, get_db
from app.crud import (
    get_datasets, 
    get_dataset_by_id, 
    create_dataset, 
    update_dataset, 
    delete_dataset
)
from app.downloader import process_zip_archive

# Create the tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dataset Management API")

# Original background task endpoint
class DownloadRequest(BaseModel):
    id: str  # Should be a string, e.g., "1"

@app.post("/download-archive")
async def download_archive(request: DownloadRequest, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(process_zip_archive, request.id)
        return {"status": "Started", "message": f"Searching for '*_{request.id}.zip' in archive_dir..."}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# New Dataset CRUD endpoints
@app.get("/datasets", response_model=List[DatasetResponse], tags=["Datasets"])
def read_datasets(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Get all datasets with optional pagination."""
    datasets = get_datasets(db, skip=skip, limit=limit)
    return datasets

@app.get("/datasets/{dataset_id}", response_model=DatasetResponse, tags=["Datasets"])
def read_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """Get a specific dataset by ID."""
    db_dataset = get_dataset_by_id(db, dataset_id=dataset_id)
    if db_dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return db_dataset

@app.post("/datasets", response_model=DatasetResponse, status_code=201, tags=["Datasets"])
def create_new_dataset(dataset: DatasetCreate, db: Session = Depends(get_db)):
    """Create a new dataset."""
    return create_dataset(db=db, dataset=dataset)

@app.put("/datasets/{dataset_id}", response_model=DatasetResponse, tags=["Datasets"])
def update_existing_dataset(
    dataset_id: int, 
    dataset: DatasetUpdate, 
    db: Session = Depends(get_db)
):
    """Update an existing dataset."""
    db_dataset = get_dataset_by_id(db, dataset_id=dataset_id)
    if db_dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return update_dataset(db=db, dataset_id=dataset_id, dataset=dataset)

@app.delete("/datasets/{dataset_id}", response_model=dict, tags=["Datasets"])
def delete_existing_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """Delete a dataset."""
    db_dataset = get_dataset_by_id(db, dataset_id=dataset_id)
    if db_dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    delete_dataset(db=db, dataset_id=dataset_id)
    return {"message": f"Dataset with id {dataset_id} successfully deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)