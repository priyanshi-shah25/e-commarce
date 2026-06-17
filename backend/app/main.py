# app/main.py

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: you can add DB init or other startup tasks here
    yield
    # Shutdown: cleanup if needed


app = FastAPI(
    title="E-Commerce API",
    description="A clean, production-ready e-commerce REST API built with FastAPI",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — adjust origins for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(api_router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
