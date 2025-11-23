from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

# Create async database engine
engine = create_async_engine(
    settings.db_url,
    pool_pre_ping=True,  # Validates DB connections before use
)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,  # Class to use in order to create new Session objects
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create async session.
    Returns an async generator that yields AsyncSession, nothing is sent back into the generator (None).
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
