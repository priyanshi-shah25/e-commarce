# app/api/v1/endpoint/orders.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.order import OrderStatus
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=list[OrderResponse])
async def get_orders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = OrderService(db)
    return await service.get_user_orders(current_user.id)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = OrderService(db)
    return await service.get_order(current_user.id, order_id)


@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(
    payload: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = OrderService(db)
    return await service.create_order(current_user.id, payload)


@router.post("/from-cart", response_model=OrderResponse, status_code=201)
async def create_order_from_cart(
    shipping_address: str = Query(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = OrderService(db)
    return await service.create_order_from_cart(current_user.id, shipping_address)


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = OrderService(db)
    return await service.update_order_status(order_id, payload.status)
