from sqlalchemy.orm import Session
from db.db.models.table_model import TableModel

def get_item_by_id(db: Session, item_id: int):
    return db.query(TableModel).filter(TableModel.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(TableModel).offset(skip).limit(limit).all()

def create_item(db: Session, name: str, description: str):
    db_item = TableModel(name=name, description=description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = get_item_by_id(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False

def update_item(db: Session, item_id: int, name: str, description: str):
    db_item = get_item_by_id(db, item_id)
    if db_item:
        db_item.name = name
        db_item.description = description
        db.commit()
        db.refresh(db_item)
        return db_item
    return None
