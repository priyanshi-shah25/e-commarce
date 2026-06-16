# app/api/v1/endpoints/products.py

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService

router = APIRouter()


@router.get("/")
async def get_products(
    db: AsyncSession = Depends(get_db),
):

    repository = ProductRepository(db)

    return await repository.get_all()