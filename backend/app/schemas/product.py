# app/schemas/product.py

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    price: Decimal
    stock: int = 0
    image_url: str | None = None
    category_id: int


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    stock: int | None = None
    image_url: str | None = None
    category_id: int | None = None
    is_active: bool | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    stock: int
    image_url: str | None
    is_active: bool
    category_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
