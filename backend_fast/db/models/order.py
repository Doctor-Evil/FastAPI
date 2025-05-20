from sqlalchemy.orm import mapped_column, Mapped, relationship
from db.database import Base
from sqlalchemy import Integer, DateTime, ForeignKey
from datetime import datetime
from enum import Enum


class OrderStatus(Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    status: Mapped[OrderStatus]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    user = relationship("User")
    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )
