from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.schemas import OrderCreate, OrderRead, OrderUpdate, OrderStatus
from db.database import get_db
from crud.orders import create_order, get_all_orders, get_order_by_id, update_order, delete_order
from utils import check_user_admin
from dependencies import get_current_user
from crud.user import get_user

router = APIRouter(tags=["orders"], prefix="/orders")


@router.post("/create", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order_endpoint(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new order.
    """
    try:
        # Check if the user exists
        user = get_user(db=db, user_id=order.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        order = create_order(db=db, order=order)
        return order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get/{order_id}", response_model=OrderRead)
def read_order_endpoint(order_id: int, db: Session = Depends(get_db)):
    """
    Get an order by ID.
    """
    try:
        order = get_order_by_id(db=db, order_id=order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        return order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/update/{order_id}", response_model=OrderRead)
def update_order_endpoint(order_id: int, order: OrderCreate, db: Session = Depends(get_db)):
    """
    Update an order by ID.
    """
    try:
        # order = get_order_by_id(db=db, order_id=order_id)
        order = update_order(db=db, order_id=order_id, order=order)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # Update the order
        return order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/delete/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_endpoint(order_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):    
    """
    Delete an order by ID.
    """
    try:
        # return print(order_id)
        # print(order)
        # order = get_order_by_id(db=db, order_id=order_id)
        # if not order:
        #     raise HTTPException(status_code=404, detail="Order not found")
        # Check if the user is an admin
        if not check_user_admin(current_user):
            updated_data = OrderUpdate(
                status=OrderStatus.cancelled
            )
            # order.status = "cancelled"
            return update_order(db=db, order=updated_data, order_id=order_id)
        
        # Delete the order
        return delete_order(db=db, order_id=order_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))    


@router.get("/list/all", response_model=list[OrderRead])
def read_orders(db: Session = Depends(get_db)):
    """
    Get all orders.
    """
    return get_all_orders(db=db)
