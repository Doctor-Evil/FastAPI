from sqlalchemy.orm import mapped_column, Mapped, relationship
from db.database import Base
from sqlalchemy import Enum as SQLAlchemyEnum
from enum import Enum


class UserRole(Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SQLAlchemyEnum(UserRole, name="userrole"), default=UserRole.user
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
