from sqlalchemy.orm import Session
from db.models.order_item import OrderItem
from db.schemas import OrderItemCreate, OrderItemRead


def create_order_item(db: Session, order_item: OrderItemCreate) -> OrderItemRead:
    db_order_item = OrderItem(**order_item.model_dump())
    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)
    return db_order_item


def get_all_order_items(db: Session) -> list[OrderItemRead]:
    order_items = db.query(OrderItem).all()
    return order_items
