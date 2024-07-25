import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserRole, UserUpdate
from app.services.user_service import UserService

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


@pytest.fixture
def user_service(async_session):
    return UserService(session=async_session)


@pytest.mark.asyncio
async def test_create_user(user_service):
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        password="hashedpassword",
        role=UserRole.USER,
        is_active=True,
    )

    user = await user_service.create_user(user_data)

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.username == "testuser"


@pytest.mark.asyncio
async def test_get_user(user_service, async_session):
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashedpassword",
        role="user",
        is_active=True,
    )
    async_session.add(user)
    await async_session.commit()

    fetched_user = await user_service.get_user(user.id)

    assert fetched_user is not None
    assert fetched_user.email == "test@example.com"


@pytest.mark.asyncio
async def test_update_user(user_service, async_session):
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashedpassword",
        role="user",
        is_active=True,
    )
    async_session.add(user)
    await async_session.commit()

    user_data = UserUpdate(
        username="updateduser",
        password="newhashedpassword",
    )

    updated_user = await user_service.update_user(user.id, user_data)

    assert updated_user.email == "test@example.com"
    assert updated_user.username == "updateduser"
    assert updated_user.hashed_password == "newhashedpassword"


@pytest.mark.asyncio
async def test_delete_user(user_service, async_session):
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashedpassword",
        role="user",
        is_active=True,
    )
    async_session.add(user)
    await async_session.commit()

    result = await user_service.delete_user(user.id)

    assert result is True
    fetched_user = await user_service.get_user(user.id)
    assert fetched_user is None
