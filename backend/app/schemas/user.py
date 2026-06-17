# app/schemas/user.py

from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
