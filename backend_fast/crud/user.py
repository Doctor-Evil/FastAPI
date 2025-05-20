from typing import Optional
from sqlalchemy.orm import Session
from db.models.user import User
from db.schemas import UserCreate, UserUpdate, UserRead
from utils import hash_password, verify_password


def create_user(db: Session, user: UserCreate) -> UserRead:
    db_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(
            user.password
        ),  # In a real application, hash the password
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(User).filter_by(id=user_id).one_or_none()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter_by(email=email).one_or_none()


def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None

    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None

    db.delete(db_user)
    db.commit()
    return db_user


def get_users(db: Session):
    return db.query(User).all()


def authenticate_user(email: str, password: str, db: Session) -> Optional[User]:
    user = get_user_by_email(email=email, db=db)
    if user is None:
        return
    if not verify_password(password, user.password):
        return
    return user
