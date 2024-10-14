from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite"

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

@asynccontextmanager
async def get_async_db_session():
    async with AsyncSessionLocal() as session:
        yield session