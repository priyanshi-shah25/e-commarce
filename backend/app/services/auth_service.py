# app/services/auth_service.py

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.exceptions import ConflictException, UnauthorizedException
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse


class AuthService:

    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def register(self, payload: RegisterRequest) -> User:
        existing = await self.user_repo.get_by_email(payload.email)
        if existing:
            raise ConflictException("Email already registered")

        user = User(
            name=payload.name,
            email=payload.email,
            password_hash=hash_password(payload.password),
        )
        return await self.user_repo.create(user)

    async def login(self, payload: LoginRequest) -> TokenResponse:
        user = await self.user_repo.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.password_hash):
            raise UnauthorizedException("Invalid email or password")

        if not user.is_active:
            raise UnauthorizedException("Account is deactivated")

        token_data = {"sub": str(user.id)}
        return TokenResponse(
            access_token=create_access_token(token_data),
            refresh_token=create_refresh_token(token_data),
        )

    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise UnauthorizedException("Invalid refresh token")

        user_id = payload.get("sub")
        user = await self.user_repo.get_by_id(int(user_id))
        if not user:
            raise UnauthorizedException("User not found")

        token_data = {"sub": str(user.id)}
        return TokenResponse(
            access_token=create_access_token(token_data),
            refresh_token=create_refresh_token(token_data),
        )
