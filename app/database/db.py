from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import get_db_url

db_url = get_db_url("asyncpg")

engine = create_async_engine(db_url, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with async_session() as session:
        yield session
