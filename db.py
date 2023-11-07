from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, engine

import settings


class DB:
    def __init__(self) -> None:
        self.engine = engine.create_async_engine(url=settings.DB_URL)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
            autocommit=False,
        )

    def get_session(self) -> AsyncSession:
        session = self.session_factory()
        return session

    async def session_dependency(self) -> AsyncSession:
        session = self.get_session()
        yield session
        await session.close()


db = DB()
