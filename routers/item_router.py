from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import ItemCreate, ItemUpdate, ItemResponse
from services import item_service

router = APIRouter(prefix="/items", tags=["items"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@router.post("/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return item_service.create_item(db, item)

@router.get("/", response_model=list[ItemResponse])
def read_items(db: Session = Depends(get_db)):
    return item_service.get_items(db)

@router.get("/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = item_service.get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item Not found")
    return db_item

@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    updated = item_service.update_item(db, item_id, item)
    if updated is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    deleted = item_service.delete_item(db, item_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message":"Item deleted successfully"}