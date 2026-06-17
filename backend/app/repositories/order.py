# app/repositories/order.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.order import Order
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):

    def __init__(self, db: AsyncSession):
        super().__init__(Order, db)

    async def get_user_orders(self, user_id: int) -> list[Order]:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
        )
        return list(result.scalars().unique().all())

    async def get_by_id_with_items(self, order_id: int) -> Order | None:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == order_id)
        )
        return result.scalar_one_or_none()
