# app/models/product.py

from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, Text, Numeric, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(default=0)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Foreign keys
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)

    # Relationships
    category: Mapped["Category"] = relationship(back_populates="products")  # noqa: F821
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="product")  # noqa: F821
    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="product")  # noqa: F821
