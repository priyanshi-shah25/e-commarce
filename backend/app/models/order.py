# app/models/order.py

import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, Numeric, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), default=OrderStatus.PENDING
    )
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    shipping_address: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Foreign keys
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="orders")  # noqa: F821
    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quantity: Mapped[int] = mapped_column(default=1)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    # Foreign keys
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)

    # Relationships
    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship(back_populates="order_items")  # noqa: F821
