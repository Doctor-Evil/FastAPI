from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from enum import Enum


class UserRole(str, Enum):
    user = "user"
    admin = "admin"


class OrderStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class OrderBase(BaseModel):
    status: Optional[OrderStatus] = OrderStatus.pending


class OrderCreate(OrderBase):
    user_id: int


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None


class OrderRead(OrderBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


class ItemCreate(ItemBase):
    owner_id: int


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class ItemRead(ItemBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True


class OrderItemBase(BaseModel):
    order_id: int
    item_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemRead(OrderItemBase):
    id: int

    class Config:
        orm_mode = True
