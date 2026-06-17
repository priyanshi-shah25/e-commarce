# app/services/order_service.py

from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException, BadRequestException
from app.models.order import Order, OrderItem, OrderStatus
from app.repositories.order import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.cart import CartRepository
from app.schemas.order import OrderCreate


class OrderService:

    def __init__(self, db: AsyncSession):
        self.order_repo = OrderRepository(db)
        self.product_repo = ProductRepository(db)
        self.cart_repo = CartRepository(db)

    async def get_user_orders(self, user_id: int) -> list[Order]:
        return await self.order_repo.get_user_orders(user_id)

    async def get_order(self, user_id: int, order_id: int) -> Order:
        order = await self.order_repo.get_by_id_with_items(order_id)
        if not order or order.user_id != user_id:
            raise NotFoundException("Order not found")
        return order

    async def create_order(self, user_id: int, payload: OrderCreate) -> Order:
        order_items = []
        total = Decimal("0.00")

        for item_data in payload.items:
            product = await self.product_repo.get_by_id(item_data.product_id)
            if not product:
                raise NotFoundException(
                    f"Product {item_data.product_id} not found"
                )
            if product.stock < item_data.quantity:
                raise BadRequestException(
                    f"Insufficient stock for {product.name}"
                )

            item_total = product.price * item_data.quantity
            total += item_total

            order_items.append(
                OrderItem(
                    product_id=product.id,
                    quantity=item_data.quantity,
                    unit_price=product.price,
                )
            )

            # Decrease stock
            await self.product_repo.update(
                product, {"stock": product.stock - item_data.quantity}
            )

        order = Order(
            user_id=user_id,
            shipping_address=payload.shipping_address,
            total_amount=total,
            items=order_items,
        )
        return await self.order_repo.create(order)

    async def create_order_from_cart(self, user_id: int, shipping_address: str) -> Order:
        cart_items = await self.cart_repo.get_user_cart(user_id)
        if not cart_items:
            raise BadRequestException("Cart is empty")

        order_items = []
        total = Decimal("0.00")

        for cart_item in cart_items:
            product = cart_item.product
            if product.stock < cart_item.quantity:
                raise BadRequestException(
                    f"Insufficient stock for {product.name}"
                )

            item_total = product.price * cart_item.quantity
            total += item_total

            order_items.append(
                OrderItem(
                    product_id=product.id,
                    quantity=cart_item.quantity,
                    unit_price=product.price,
                )
            )

            await self.product_repo.update(
                product, {"stock": product.stock - cart_item.quantity}
            )

        order = Order(
            user_id=user_id,
            shipping_address=shipping_address,
            total_amount=total,
            items=order_items,
        )
        created_order = await self.order_repo.create(order)

        # Clear cart after order
        await self.cart_repo.clear_cart(user_id)

        return created_order

    async def update_order_status(
        self, order_id: int, status: OrderStatus
    ) -> Order:
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise NotFoundException("Order not found")
        return await self.order_repo.update(order, {"status": status})
