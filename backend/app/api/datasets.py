from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.file_service import list_datasets, get_file_response

router = APIRouter()

class DownloadRequest(BaseModel):
    file_id: str
    format: str

@router.get("/", summary="List available datasets")
async def list_all():
    """Return list of files in the datasets directory"""
    files = await list_datasets()
    return {"datasets": files}

@router.post("/download/", summary="Download a dataset by file_id and format")
async def download(req: DownloadRequest):
    """Stream a file from server storage to user"""
    try:
        return await get_file_response(req.file_id, req.format)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))