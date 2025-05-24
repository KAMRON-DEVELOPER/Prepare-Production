import asyncio
from typing import Annotated, AsyncGenerator
from uuid import UUID, uuid4

from fastapi import Depends
from sqlalchemy import TIMESTAMP, String, func, UUID as PG_UUID
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.my_config import get_settings


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid4, primary_key=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), default=func.now())
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now())


settings = get_settings()

# Use get_secret_value() for Pydantic SecretStr
if not settings.DB_URL:
    raise ValueError("DB_URL must be set")

if not settings.REDIS_URL:
    raise ValueError("REDIS_URL must be set")

async_engine: AsyncEngine = create_async_engine(settings.DB_URL, echo=False)
async_session = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


DBSession = Annotated[AsyncSession, Depends(get_session)]


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class UserModel(BaseModel):
    __tablename__ = "user_table_extra"
    username: Mapped[str] = mapped_column(String(length=50), index=True)
    email: Mapped[str] = mapped_column(String(length=50), index=True)
    password: Mapped[str] = mapped_column(String(length=120))


if __name__ == "__main__":
    asyncio.run(init_db())
