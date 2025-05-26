from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.schemas import ItemCreate, ItemRead, ItemUpdate
from db.database import get_db
from crud.items import create_item, get_all_items, get_item_by_id, update_item, delete_item
from dependencies import get_current_user
from utils import check_user_admin
from crud.user import get_user

router = APIRouter(tags=["items"], prefix="/items")


@router.post("/create", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item_endpoint(item: ItemCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Create a new item.
    """
    try:
        # Check if the user is an admin
        if not check_user_admin(current_user):
            raise HTTPException(status_code=403, detail="Not enough permissions")
        
        # Check if the user exists
        user = get_user(db=db, user_id=item.owner_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return create_item(db=db, item=item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/list/all", response_model=list[ItemRead])
def read_items(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Get all items.
    """
    # Check if the user is an admin
    if not check_user_admin(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return get_all_items(db=db)

@router.get("/get/{item_id}", response_model=ItemRead)
def read_item(item_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Get an item by ID.
    """
    # Check if the user is an admin
    if not check_user_admin(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    try:
        item = get_item_by_id(db=db, item_id=item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
    
        return item
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/update/{item_id}", response_model=ItemUpdate)
def update_item_endpoint(item_id: int, item: ItemUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Update an item by ID.
    """
    # Check if the user is an admin
    if not check_user_admin(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    try:
        updated_item = update_item(db=db, item_id=item_id, item=item)
        if not updated_item:
            raise HTTPException(status_code=404, detail="Item not found")
    
        return updated_item
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 

@router.delete("/delete/{item_id}", response_model=ItemRead)
def delete_item_endpoint(item_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Delete an item by ID.
    """
    # Check if the user is an admin
    if not check_user_admin(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    try:
        deleted_item = delete_item(db=db, item_id=item_id)
        if not deleted_item:
            raise HTTPException(status_code=404, detail="Item not found")
    
        return deleted_item
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))   