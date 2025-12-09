import logging
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from app.core.config import settings

logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping = True,
    pool_size = 10,
    max_overflow = 10
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise 
        finally:
            await session.close()