from sqlalchemy.orm import Session
from models import Item
from schemas import ItemCreate, ItemUpdate

def get_items(db: Session):
    return db.query(Item).all()

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def create_item(db: Session, item: ItemCreate):
    new_item = Item(name=item.name, description = item.description)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def update_item(db: Session, item_id: int, new_item: ItemUpdate):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        return None
    db_item.name = new_item.name
    db_item.description = new_item.description
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        return None
    db.delete(db_item)
    db.commit()
    return db_item