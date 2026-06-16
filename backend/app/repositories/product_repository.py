# app/repositories/product_repository.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product


class ProductRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(
            select(Product)
        )

        return result.scalars().all()

    async def get_by_id(self, product_id: int):
        result = await self.db.execute(
            select(Product).where(
                Product.id == product_id
            )
        )

        return result.scalar_one_or_none()

    async def create(self, product: Product):
        self.db.add(product)

        await self.db.commit()

        await self.db.refresh(product)

        return product