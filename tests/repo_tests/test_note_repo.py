import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.models.note_model import Note
from app.models.user_model import User
from app.repos import NoteRepository

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
async def test_create_note(async_session):
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashedpassword",
        role="user",
        is_active=True,
    )
    async_session.add(user)
    await async_session.commit()

    note_repo = NoteRepository(async_session)

    note = Note(title="Test Note", content="This is a test note.", owner_id=user.id)

    created_note = await note_repo.create_note(note)

    assert created_note.id is not None
    assert created_note.title == "Test Note"
    assert created_note.content == "This is a test note."
    assert created_note.owner_id == user.id


@pytest.mark.asyncio
async def test_get_note(async_session):
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashedpassword",
        role="user",
        is_active=True,
    )
    async_session.add(user)
    await async_session.commit()

    note_repo = NoteRepository(async_session)

    note = Note(title="Test Note", content="This is a test note.", owner_id=user.id)
    await note_repo.create_note(note)

    fetched_note = await note_repo.get_note(note.id)

    assert fetched_note is not None
    assert fetched_note.title == "Test Note"
    assert fetched_note.content == "This is a test note."


@pytest.mark.asyncio
async def test_get_notes_by_user_id(async_session):
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashedpassword",
        role="user",
        is_active=True,
    )
    async_session.add(user)
    await async_session.commit()

    note_repo = NoteRepository(async_session)

    note1 = Note(
        title="Test Note 1", content="This is the first test note.", owner_id=user.id
    )
    note2 = Note(
        title="Test Note 2", content="This is the second test note.", owner_id=user.id
    )
    await note_repo.create_note(note1)
    await note_repo.create_note(note2)

    notes = await note_repo.get_notes_by_user_id(user.id)

    assert len(notes) == 2
    assert any(note.title == "Test Note 1" for note in notes)
    assert any(note.title == "Test Note 2" for note in notes)


@pytest.mark.asyncio
async def test_update_note(async_session):
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashedpassword",
        role="user",
        is_active=True,
    )
    async_session.add(user)
    await async_session.commit()

    note_repo = NoteRepository(async_session)

    note = Note(title="Old Title", content="Old content.", owner_id=user.id)
    created_note = await note_repo.create_note(note)

    created_note.title = "Updated Title"
    created_note.content = "Updated content."
    updated_note = await note_repo.update_note(created_note)

    assert updated_note.title == "Updated Title"
    assert updated_note.content == "Updated content."


@pytest.mark.asyncio
async def test_delete_note(async_session):
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashedpassword",
        role="user",
        is_active=True,
    )
    async_session.add(user)
    await async_session.commit()

    note_repo = NoteRepository(async_session)

    note = Note(
        title="Note to Delete", content="This note will be deleted.", owner_id=user.id
    )
    created_note = await note_repo.create_note(note)

    await note_repo.delete_note(created_note)

    fetched_note = await note_repo.get_note(created_note.id)
    assert fetched_note is None
