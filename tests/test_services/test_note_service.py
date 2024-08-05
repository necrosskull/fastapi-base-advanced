import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.models.note_model import Note
from app.models.user_model import User
from app.repos.note_repo import NoteRepository
from app.schemas.note_schema import NoteCreate, NoteUpdate
from app.services import NoteService

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
def note_repo(async_session):
    return NoteRepository(async_session)


@pytest.fixture
def note_service(note_repo):
    return NoteService(note_repo)


@pytest.mark.asyncio
async def test_create_note(note_service, async_session):
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashedpassword",
        role="user",
        is_active=True,
    )
    async_session.add(user)
    await async_session.commit()

    note_data = NoteCreate(
        title="Test Note", content="This is a test note.", owner_id=user.id
    )

    note = await note_service.create_note(note_data)

    assert note.id is not None
    assert note.title == "Test Note"
    assert note.content == "This is a test note."
    assert note.owner_id == user.id


@pytest.mark.asyncio
async def test_get_note(note_service, async_session):
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashedpassword",
        role="user",
        is_active=True,
    )
    async_session.add(user)
    await async_session.commit()

    note = Note(title="Test Note", content="This is a test note.", owner_id=user.id)
    async_session.add(note)
    await async_session.commit()

    fetched_note = await note_service.get_note(note.id)

    assert fetched_note is not None
    assert fetched_note.title == "Test Note"
    assert fetched_note.content == "This is a test note."


@pytest.mark.asyncio
async def test_update_note(note_service, async_session):
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashedpassword",
        role="user",
        is_active=True,
    )
    async_session.add(user)
    await async_session.commit()

    note = Note(title="Old Title", content="Old content.", owner_id=user.id)
    async_session.add(note)
    await async_session.commit()

    note_data = NoteUpdate(title="Updated Title")

    updated_note = await note_service.update_note(note.id, note_data)

    assert updated_note.title == "Updated Title"
    assert updated_note.content == "Old content."


@pytest.mark.asyncio
async def test_delete_note(note_service, async_session):
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashedpassword",
        role="user",
        is_active=True,
    )
    async_session.add(user)
    await async_session.commit()

    note = Note(
        title="Note to Delete", content="This note will be deleted.", owner_id=user.id
    )
    async_session.add(note)
    await async_session.commit()

    result = await note_service.delete_note(note.id)

    assert result is True
    fetched_note = await note_service.get_note(note.id)
    assert fetched_note is None
