import os
import shutil
from urllib.parse import quote
from fastapi import BackgroundTasks

DATA_ROOT = "data_storage"
ARCHIVE_OUTPUT_DIR = "archives"
os.makedirs(ARCHIVE_OUTPUT_DIR, exist_ok=True)


async def archive_directory_stream(dirname: str) -> str:
    dir_path = os.path.join(DATA_ROOT, dirname)
    
    if not os.path.isdir(dir_path):
        raise FileNotFoundError(f"Directory '{dirname}' does not exist.")

    base_output_path = os.path.join(DATA_ROOT, dirname)  # No .zip
    zip_path = base_output_path + ".zip"

    # Ensure it always creates the ZIP, even for empty folders
    shutil.make_archive(base_output_path, 'zip', dir_path)

    return zip_path


def list_files_with_links(dirname: str, base_url: str) -> list:
    dir_path = os.path.join(DATA_ROOT, dirname)
    if not os.path.isdir(dir_path):
        raise FileNotFoundError(f"Directory '{dirname}' does not exist.")

    files = []
    for fname in os.listdir(dir_path):
        fpath = os.path.join(dir_path, fname)
        if os.path.isfile(fpath):
            download_url = f"{base_url}static/{quote(dirname)}/{quote(fname)}"
            files.append({
                "filename": fname,
                "download_link": download_url
            })
    return files
