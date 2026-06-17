# app/services/product_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundException
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:

    def __init__(self, db: AsyncSession):
        self.repo = ProductRepository(db)

    async def get_products(
        self, page: int = 1, limit: int = 20, category_id: int | None = None
    ):
        skip = (page - 1) * limit
        products = await self.repo.get_all(
            skip=skip, limit=limit, category_id=category_id
        )
        total = await self.repo.count(category_id=category_id)
        return {
            "items": products,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit,
        }

    async def get_product(self, product_id: int) -> Product:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise NotFoundException("Product not found")
        return product

    async def create_product(self, payload: ProductCreate) -> Product:
        product = Product(**payload.model_dump())
        return await self.repo.create(product)

    async def update_product(
        self, product_id: int, payload: ProductUpdate
    ) -> Product:
        product = await self.get_product(product_id)
        update_data = payload.model_dump(exclude_unset=True)
        return await self.repo.update(product, update_data)

    async def delete_product(self, product_id: int) -> None:
        product = await self.get_product(product_id)
        await self.repo.delete(product)
