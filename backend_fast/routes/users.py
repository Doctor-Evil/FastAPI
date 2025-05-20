from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.schemas import UserCreate, UserRead, UserUpdate
from crud.user import create_user, get_user, get_users, update_user, get_user_by_email
from utils import check_user_admin
from dependencies import get_current_user

from typing import Annotated

router = APIRouter(tags=["users"], prefix="/users")


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=UserRead)
def create_user_endpoint(
    form_data: Annotated[UserCreate, Depends()], db: Session = Depends(get_db)
):
    """
    Create a new user.
    """
    try:
        existing_user = get_user_by_email(db=db, email=form_data.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        return create_user(db=db, user=form_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/get/{user_id}")
def read_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user by ID.
    """
    user = get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


@router.put("/update/{user_id}", response_model=UserUpdate)
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """
    Update a user by ID.
    """
    updated_user = update_user(db=db, user_id=user_id, user=user)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return updated_user


@router.delete("/delete/{user_id}")
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Delete a user by ID.
    """
    user = get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    elif not check_user_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't delete a user because you are not an admin",
        )

    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}


@router.get("/list/all", response_model=list[UserRead])
def read_users(
    db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    """
    Get all users.
    """
    if not check_user_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )

    return get_users(db=db)


@router.get("/me")
def read_me_endpoint(db: Session = Depends(get_db)):
    """
    Get the current user.
    """
    # Assuming you have a way to get the current user from the request
    # For example, using JWT token or session
    current_user = get_current_user(db=db)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    return current_user
