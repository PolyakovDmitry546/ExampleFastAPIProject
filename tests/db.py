import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from models import Base


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite://"  # Путь для создания базы данных в памяти.
                                                 # После закрытия подключения база данных удаляется.


class InmemorySqlite():
    def __init__(self) -> None:
        self.engine = create_async_engine(
            SQLALCHEMY_DATABASE_URL,
            connect_args={"check_same_thread": False},  # Отключает проверку однопоточного доступа в Sqlite
            poolclass=StaticPool,
        )

        self.session_factory = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def async_init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def async_drop_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    def init_db(self):
        asyncio.run(self.async_init_db())

    def drop_db(self):
        asyncio.run(self.async_drop_db())

    def get_session(self) -> AsyncSession:
        return self.session_factory()

    def session_dependency(self):
        try:
            session = self.session_factory()
            yield session
        finally:
            session.close()


def init_test_inmemory_sqlite_decorator(db: InmemorySqlite):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            await db.async_init_db()
            try:
                return_value = await func(*args, **kwargs)
            finally:
                await db.async_drop_db()
            return return_value
        return wrapper
    return decorator
