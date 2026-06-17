# app/repositories/product_repository.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.product import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):

    def __init__(self, db: AsyncSession):
        super().__init__(Product, db)

    async def get_all(
        self, skip: int = 0, limit: int = 20, category_id: int | None = None
    ) -> list[Product]:
        query = select(Product).options(selectinload(Product.category))

        if category_id is not None:
            query = query.where(Product.category_id == category_id)

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().unique().all())

    async def get_by_id(self, id: int) -> Product | None:
        result = await self.db.execute(
            select(Product)
            .options(selectinload(Product.category))
            .where(Product.id == id)
        )
        return result.scalar_one_or_none()

    async def count(self, category_id: int | None = None) -> int:
        from sqlalchemy import func

        query = select(func.count()).select_from(Product)
        if category_id is not None:
            query = query.where(Product.category_id == category_id)
        result = await self.db.execute(query)
        return result.scalar_one()
