# app/api/v1/api.py

from fastapi import APIRouter

from app.api.v1.endpoint import auth, products, categories, cart, orders

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(products.router)
router.include_router(categories.router)
router.include_router(cart.router)
router.include_router(orders.router)
