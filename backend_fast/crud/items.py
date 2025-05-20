from typing import Optional
from sqlalchemy.orm import Session
from db.models.item import Item
from db.schemas import ItemCreate, ItemRead
from datetime import datetime


def create_item(db: Session, item: ItemCreate) -> ItemRead:
    db_item = Item(
        name=item.name,
        description=item.description,
        owner_id=item.owner_id,
        price=item.price,
        created_at=datetime.now(),
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item_by_id(db: Session, item_id: int) -> Optional[ItemRead]:
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return None
    return item


def get_all_items(db: Session) -> list[ItemRead]:
    items = db.query(Item).all()
    return items

def update_item(db: Session, item_id: int, item: ItemCreate) -> Optional[ItemRead]:
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        return None

    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int) -> Optional[ItemRead]:
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        return None

    db.delete(db_item)
    db.commit()
    return db_item