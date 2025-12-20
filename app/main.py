import uvicorn
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from app.api.api import api_router
from app.core.config import settings
from app.core.logger import configure_uvicorn_logging, logger, setup_logger, shutdown_logger
from app.middleware.logging import LoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""

    logger.info("Initializing resources before the app start...")
    setup_logger()
    configure_uvicorn_logging()
    logger.success("Resources initialized.")

    yield  # Application runs here

    logger.info("Cleaning up resources on app shutdown...")
    shutdown_logger()
    logger.success("Resources cleaned up.")


app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(LoggingMiddleware)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8000,
    )
