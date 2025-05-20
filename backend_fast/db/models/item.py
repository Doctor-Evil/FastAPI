import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from db.database import Base


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    price: Mapped[float] = mapped_column(nullable=False, default=0.0)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.timezone.utc)

    owner = relationship("User")
    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="item", cascade="all, delete-orphan"
    )
