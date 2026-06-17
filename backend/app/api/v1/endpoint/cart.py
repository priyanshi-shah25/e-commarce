# app/api/v1/endpoint/cart.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemUpdate, CartItemResponse
from app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/", response_model=list[CartItemResponse])
async def get_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CartService(db)
    return await service.get_cart(current_user.id)


@router.post("/", response_model=CartItemResponse, status_code=201)
async def add_to_cart(
    payload: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CartService(db)
    return await service.add_to_cart(
        current_user.id, payload.product_id, payload.quantity
    )


@router.put("/{cart_item_id}", response_model=CartItemResponse)
async def update_cart_item(
    cart_item_id: int,
    payload: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CartService(db)
    return await service.update_cart_item(
        current_user.id, cart_item_id, payload.quantity
    )


@router.delete("/{cart_item_id}", status_code=204)
async def remove_from_cart(
    cart_item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CartService(db)
    await service.remove_from_cart(current_user.id, cart_item_id)


@router.delete("/", status_code=204)
async def clear_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CartService(db)
    await service.clear_cart(current_user.id)
