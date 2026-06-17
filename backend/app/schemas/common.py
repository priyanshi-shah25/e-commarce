# app/schemas/common.py

from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: int = 1
    limit: int = 20


class PaginatedResponse(BaseModel):
    total: int
    page: int
    limit: int
    pages: int
