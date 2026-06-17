# app/services/cart_service.py

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException, BadRequestException
from app.models.cart import CartItem
from app.repositories.cart import CartRepository
from app.repositories.product_repository import ProductRepository


class CartService:

    def __init__(self, db: AsyncSession):
        self.cart_repo = CartRepository(db)
        self.product_repo = ProductRepository(db)

    async def get_cart(self, user_id: int) -> list[CartItem]:
        return await self.cart_repo.get_user_cart(user_id)

    async def add_to_cart(
        self, user_id: int, product_id: int, quantity: int = 1
    ) -> CartItem:
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundException("Product not found")

        if product.stock < quantity:
            raise BadRequestException("Insufficient stock")

        # Check if item already in cart
        existing = await self.cart_repo.get_cart_item(user_id, product_id)
        if existing:
            existing.quantity += quantity
            return await self.cart_repo.update(existing, {"quantity": existing.quantity})

        cart_item = CartItem(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
        )
        return await self.cart_repo.create(cart_item)

    async def update_cart_item(
        self, user_id: int, cart_item_id: int, quantity: int
    ) -> CartItem:
        item = await self.cart_repo.get_by_id(cart_item_id)
        if not item or item.user_id != user_id:
            raise NotFoundException("Cart item not found")

        if quantity <= 0:
            await self.cart_repo.delete(item)
            return item

        return await self.cart_repo.update(item, {"quantity": quantity})

    async def remove_from_cart(self, user_id: int, cart_item_id: int) -> None:
        item = await self.cart_repo.get_by_id(cart_item_id)
        if not item or item.user_id != user_id:
            raise NotFoundException("Cart item not found")
        await self.cart_repo.delete(item)

    async def clear_cart(self, user_id: int) -> None:
        await self.cart_repo.clear_cart(user_id)
