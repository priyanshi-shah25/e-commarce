# app/repositories/cart.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.cart import CartItem
from app.repositories.base import BaseRepository


class CartRepository(BaseRepository[CartItem]):

    def __init__(self, db: AsyncSession):
        super().__init__(CartItem, db)

    async def get_user_cart(self, user_id: int) -> list[CartItem]:
        result = await self.db.execute(
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(CartItem.user_id == user_id)
        )
        return list(result.scalars().unique().all())

    async def get_cart_item(
        self, user_id: int, product_id: int
    ) -> CartItem | None:
        result = await self.db.execute(
            select(CartItem).where(
                CartItem.user_id == user_id,
                CartItem.product_id == product_id,
            )
        )
        return result.scalar_one_or_none()

    async def clear_cart(self, user_id: int) -> None:
        result = await self.db.execute(
            select(CartItem).where(CartItem.user_id == user_id)
        )
        items = result.scalars().all()
        for item in items:
            await self.db.delete(item)
        await self.db.commit()
