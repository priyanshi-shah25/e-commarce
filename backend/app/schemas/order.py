# app/schemas/order.py

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.models.order import OrderStatus


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class OrderCreate(BaseModel):
    shipping_address: str
    items: list[OrderItemCreate]


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: int
    status: OrderStatus
    total_amount: Decimal
    shipping_address: str
    items: list[OrderItemResponse]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
