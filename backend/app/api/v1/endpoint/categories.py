# app/api/v1/endpoint/categories.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    service = CategoryService(db)
    return await service.get_categories()


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    service = CategoryService(db)
    return await service.get_category(category_id)


@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(
    payload: CategoryCreate, db: AsyncSession = Depends(get_db)
):
    service = CategoryService(db)
    return await service.create_category(payload)


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    payload: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = CategoryService(db)
    return await service.update_category(category_id, payload)


@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    service = CategoryService(db)
    await service.delete_category(category_id)
