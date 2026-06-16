# app/models/product.py

from decimal import Decimal

from sqlalchemy import (
    String,
    Numeric,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
    )

    description: Mapped[str] = mapped_column()

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
    )

    stock: Mapped[int] = mapped_column(
        default=0,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
    )

    category = relationship(
        "Category",
        back_populates="products",
    )