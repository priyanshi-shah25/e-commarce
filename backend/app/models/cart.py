# app/models/cart.py

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quantity: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Foreign keys
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="cart_items")  # noqa: F821
    product: Mapped["Product"] = relationship(back_populates="cart_items")  # noqa: F821
