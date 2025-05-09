from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from app.services.fileservice import archive_directory_stream, list_files_with_links
from app.models import Base
from app.schemas import DatasetCreate, DatasetUpdate, DatasetResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, get_db
from app.crud import (
    get_datasets, 
    get_dataset_by_id, 
    create_dataset, 
    update_dataset, 
    delete_dataset
)
import os
from app.downloader import process_zip_archive
class DirectoryRequest(BaseModel):
    dirname: str

from fastapi.middleware.cors import CORSMiddleware
# Create the tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dataset Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="data_storage"), name="static")

# Original background task endpoint
class DownloadRequest(BaseModel):
    id: str  # Should be a string, e.g., "1"

@app.post("/download")
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

@app.post("/archive-and-download")
async def archive_and_download(request: DirectoryRequest, background_tasks: BackgroundTasks):
    dirname = request.dirname.replace(" ", "_")
    
    archive_path = await archive_directory_stream(dirname)
    print("saad alam:", archive_path)
    if not archive_path or not os.path.exists(archive_path):
        raise HTTPException(status_code=404, detail=f"Directory '{dirname}' not found or archiving failed.")

    def file_iterator():
        with open(archive_path, "rb") as f:
            yield from f

    filename = os.path.basename(archive_path)
    return StreamingResponse(
        file_iterator(),
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@app.post("/list-files")
async def list_files(request: DirectoryRequest, req: Request):
    try:
        base_url = str(req.base_url)
        files = list_files_with_links(request.dirname, base_url)
        return JSONResponse(content={"files": files})
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Directory '{request.dirname}' not found.")



# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)