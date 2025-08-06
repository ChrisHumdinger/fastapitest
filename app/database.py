from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

DATABASE_URL = os.getenv(
   "DATABASE_URL",
   "postgresql+asyncpg://postgres:Vj9rFBQsAhmVzoHY96iT8xjMBejszoOzLqBQCbSu6ceodbjLT9zVjp1zzDjLi1az@31.97.148.167:5512/postgres"
)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()
