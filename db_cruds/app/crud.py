from sqlalchemy.orm import Session
from . import models, schemas

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
    return db_dataset

def update_dataset(db: Session, dataset_id: int, dataset: schemas.DatasetUpdate):
    """Update an existing dataset."""
    db_dataset = get_dataset_by_id(db, dataset_id)
    
    # Filter out None values to only update fields that were provided
    update_data = {k: v for k, v in dataset.model_dump().items() if v is not None}
    
    for key, value in update_data.items():
        setattr(db_dataset, key, value)
    
    db.commit()
    db.refresh(db_dataset)
    return db_dataset

def delete_dataset(db: Session, dataset_id: int):
    """Delete a dataset."""
    db_dataset = get_dataset_by_id(db, dataset_id)
    db.delete(db_dataset)
    db.commit()
    return True