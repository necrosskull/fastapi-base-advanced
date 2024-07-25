import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.models.user_model import User
from app.repos import UserRepository

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/testdb"


@pytest.fixture
async def engine():
    engine = create_async_engine(DATABASE_URL, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)

    yield engine

    await engine.dispose()

    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.drop_all)


@pytest.fixture
async def async_session(engine):
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        yield session
        await session.close()


@pytest.mark.asyncio
async def test_create_user(async_session):
    repo = UserRepository(async_session)

    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashedpassword",
        role="user",
        is_active=True,
    )

    created_user = await repo.create_user(user)

    assert created_user.id is not None
    assert created_user.email == "test@example.com"
    assert created_user.username == "testuser"
    assert created_user.role == "user"
    assert created_user.is_active is True


@pytest.mark.asyncio
async def test_get_user_by_email(async_session):
    repo = UserRepository(async_session)

    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashedpassword",
        role="user",
        is_active=True,
    )

    await repo.create_user(user)
    fetched_user = await repo.get_user_by_email("test@example.com")

    assert fetched_user is not None
    assert fetched_user.email == "test@example.com"


@pytest.mark.asyncio
async def test_update_user(async_session):
    repo = UserRepository(async_session)

    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashedpassword",
        role="user",
        is_active=True,
    )

    created_user = await repo.create_user(user)
    created_user.is_active = False
    updated_user = await repo.update_user(created_user)

    assert updated_user.is_active is False


@pytest.mark.asyncio
async def test_delete_user(async_session):
    repo = UserRepository(async_session)

    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashedpassword",
        role="user",
        is_active=True,
    )

    created_user = await repo.create_user(user)
    await repo.delete_user(created_user)

    fetched_user = await repo.get_user_by_email("test@example.com")
    assert fetched_user is None
