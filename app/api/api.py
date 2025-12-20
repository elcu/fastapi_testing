from fastapi import APIRouter

from app.domains.infrastructure.router import router as infrastructure_router

api_router = APIRouter()

api_router.include_router(infrastructure_router)
