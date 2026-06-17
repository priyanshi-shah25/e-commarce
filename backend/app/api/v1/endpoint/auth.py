# app/api/v1/endpoint/auth.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, RefreshTokenRequest
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    user = await service.register(payload)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.login(payload)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(payload: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.refresh_token(payload.refresh_token)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
