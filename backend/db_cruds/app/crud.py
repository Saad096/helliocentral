from sqlalchemy.orm import Session
from . import models, schemas
import os
import shutil

def get_datasets(db: Session, skip: int = 0, limit: int = 100):
    """Get all datasets with pagination."""
    return db.query(models.Dataset).offset(skip).limit(limit).all()

def get_dataset_by_id(db: Session, dataset_id: int):
    """Get a single dataset by its ID."""
    return db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()

def create_dataset(db: Session, dataset: schemas.DatasetCreate):
    """Create a new dataset."""
    db_dataset = models.Dataset(**dataset.model_dump())
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    os.makedirs(os.path.join("data_storage", db_dataset.name.replace(" ", "_")), exist_ok=True)
    return db_dataset

def update_dataset(db: Session, dataset_id: int, dataset: schemas.DatasetUpdate):
    """Update an existing dataset."""
    db_dataset = get_dataset_by_id(db, dataset_id)
    old_dataset_name = db_dataset.name
    
    # Filter out None values to only update fields that were provided
    update_data = {k: v for k, v in dataset.model_dump().items() if v is not None}
    
    for key, value in update_data.items():
        setattr(db_dataset, key, value)
    
    db.commit()
    db.refresh(db_dataset)
    # Make sure the folder exists before renaming
    if os.path.exists(os.path.join("data_storage", old_dataset_name)):
        os.rename(os.path.join("data_storage", old_dataset_name), os.path.join("data_storage", dataset.name.replace(" ", "_")))
        print(f"Renamed folder to: {db_dataset.name.replace(' ', '_')}")
    else:
        print(os.path.join("data_storage", old_dataset_name))
        print(f"Folder does not exist.")
    return db_dataset

def delete_dataset(db: Session, dataset_id: int):
    """Delete a dataset."""
    db_dataset = get_dataset_by_id(db, dataset_id)
    db.delete(db_dataset)
    db.commit()
    shutil.rmtree(os.path.join("data_storage", db_dataset.name.replace(" ", "_")), ignore_errors=True)
    return True