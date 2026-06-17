# app/dependencies/auth.py

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.core.exceptions import UnauthorizedException
from app.database.session import get_db
from app.models.user import User
from app.repositories.user import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise UnauthorizedException("Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Invalid token payload")

    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(int(user_id))
    if not user:
        raise UnauthorizedException("User not found")

    return user
