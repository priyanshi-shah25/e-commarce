# app/services/category_service.py

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException, ConflictException
from app.models.category import Category
from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:

    def __init__(self, db: AsyncSession):
        self.repo = CategoryRepository(db)

    async def get_categories(self):
        return await self.repo.get_all(limit=100)

    async def get_category(self, category_id: int) -> Category:
        category = await self.repo.get_by_id(category_id)
        if not category:
            raise NotFoundException("Category not found")
        return category

    async def create_category(self, payload: CategoryCreate) -> Category:
        existing = await self.repo.get_by_name(payload.name)
        if existing:
            raise ConflictException("Category with this name already exists")

        category = Category(**payload.model_dump())
        return await self.repo.create(category)

    async def update_category(
        self, category_id: int, payload: CategoryUpdate
    ) -> Category:
        category = await self.get_category(category_id)
        update_data = payload.model_dump(exclude_unset=True)
        return await self.repo.update(category, update_data)

    async def delete_category(self, category_id: int) -> None:
        category = await self.get_category(category_id)
        await self.repo.delete(category)
