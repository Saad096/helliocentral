import os
from fastapi.responses import FileResponse
from app.core.config import DATA_DIR
from app.models.dataset import Dataset

async def list_datasets():
    items = []
    for root, _, files in os.walk(DATA_DIR):
        for fname in files:
            path = os.path.join(root, fname)
            stat = os.stat(path)
            fmt = fname.split('.')[-1]
            items.append({
                'file_id': fname,
                'name': fname,
                'size': stat.st_size,
                'format': fmt
            })
    return items

async def get_file_response(file_id: str, fmt: str):
    expected = os.path.join(DATA_DIR, fmt, file_id)
    print("expected:", expected)
    
    if not os.path.isfile(expected):
        raise FileNotFoundError
    return FileResponse(
        path=expected,
        filename=file_id,
        media_type='application/octet-stream'
    )