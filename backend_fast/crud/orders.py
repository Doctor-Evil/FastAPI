from sqlalchemy.orm import Session
from db.models.order import Order
from db.schemas import OrderCreate, OrderRead, OrderUpdate
from datetime import datetime
from typing import Union, Optional


def create_order(db: Session, order: OrderCreate) -> OrderRead:
    db_order = Order(
        user_id=order.user_id,
        status=order.status,
        created_at=datetime.now(),
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_all_orders(db: Session) -> list[OrderRead]:
    orders = db.query(Order).all()
    return orders


def get_order_by_id(db: Session, order_id: int) -> OrderRead:
    order = db.query(Order).filter(Order.id == order_id).first()
    return order

def update_order(db: Session, order_id: int, order: Union[OrderCreate, OrderUpdate]) -> OrderRead:
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        return None

    for key, value in order.model_dump(exclude_unset=True).items():
        setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int) -> OrderRead:
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        return None

    db.delete(db_order)
    db.commit()
    return db_order