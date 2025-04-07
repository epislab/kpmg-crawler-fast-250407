from typing import Optional
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

class Database:
    _instance: Optional['Database'] = None
    _engine: Optional[AsyncEngine] = None
    _async_session: Optional[sessionmaker] = None

    def __new__(cls) -> 'Database':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._engine:
            DATABASE_URL = os.getenv(
                'DATABASE_URL',
                "postgresql+asyncpg://postgres:YLkbHpjtkasEeLizyLxNUvtdPSlkpNaa@crossover.proxy.rlwy.net:27041/railway"
            )
            self._engine = create_async_engine(
                DATABASE_URL,
                echo=True,
                pool_pre_ping=True,
                pool_size=5,
                max_overflow=10
            )
            self._async_session = sessionmaker(
                self._engine,
                class_=AsyncSession,
                expire_on_commit=False
            )

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @property
    def session(self) -> AsyncSession:
        return self._async_session()

    async def close(self):
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._async_session = None

# 싱글톤 인스턴스 생성
database = Database()
