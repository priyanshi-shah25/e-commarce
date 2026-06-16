# app/services/product_service.py

from app.models.product import Product


class ProductService:

    def __init__(self, repository):
        self.repository = repository

    async def create_product(
        self,
        payload,
    ):
        product = Product(
            **payload.model_dump()
        )

        return await self.repository.create(
            product
        )