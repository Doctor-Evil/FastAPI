from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.schemas import OrderItemCreate, OrderItemRead
from db.database import get_db
from crud.order_items import create_order_item, get_all_order_items
from crud.orders import get_order_by_id
from crud.items import get_item_by_id

router = APIRouter(tags=["order_items"], prefix="/order_items")


@router.post(
    "/create", response_model=OrderItemRead, status_code=status.HTTP_201_CREATED
)
def create_order_item_endpoint(
    order_item: OrderItemCreate, db: Session = Depends(get_db)
):
    """
    Create a new order item.
    """
    try:
        # Check if the order exists
        order = get_order_by_id(db=db, order_id=order_item.order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # Check if the item exists
        item = get_item_by_id(db=db, item_id=order_item.item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        return create_order_item(db=db, order_item=order_item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/list/all", response_model=list[OrderItemRead])
def read_order_items(db: Session = Depends(get_db)):
    """
    Get all order items.
    """
    return get_all_order_items(db=db)
