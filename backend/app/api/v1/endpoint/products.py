# app/api/v1/endpoint/products.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=dict)
async def get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    service = ProductService(db)
    return await service.get_products(page=page, limit=limit, category_id=category_id)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.get_product(product_id)


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    payload: ProductCreate, db: AsyncSession = Depends(get_db)
):
    service = ProductService(db)
    return await service.create_product(payload)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = ProductService(db)
    return await service.update_product(product_id, payload)


@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    await service.delete_product(product_id)
