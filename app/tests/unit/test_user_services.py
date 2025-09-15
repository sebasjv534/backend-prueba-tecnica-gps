import pytest
from unittest.mock import Mock, AsyncMock
from types import SimpleNamespace
from uuid import UUID
from datetime import datetime

from app.application.services.user_service import UserService
from app.domain.schemas.user_schema import UserCreate
from app.application.exceptions import AuthenticationError, ConflictError
from app.domain.models.user_model import User


class MockUserRepository:
    def __init__(self):
        self._users = {}
        self._users_by_email = {}

    async def get_by_username(self, username: str):
        return self._users.get(username)

    async def get_by_email(self, email: str):
        return self._users_by_email.get(email)

    async def get_by_id(self, user_id: str):
        for user in self._users.values():
            if str(user.id) == user_id:
                return user
        return None

    async def create(self, user: User):
        # Simular creación de usuario con ID
        user.id = "550e8400-e29b-41d4-a716-446655440000"
        user.created_at = datetime.utcnow()
        
        self._users[user.username] = user
        self._users_by_email[user.email] = user
        return user


@pytest.mark.asyncio
async def test_register_user_success():
    """Test successful user registration."""
    repo = MockUserRepository()
    service = UserService(repo)

    user_data = UserCreate(
        username="alice",
        email="alice@example.com",
        password="securepassword123"
    )

    created_user = await service.register_user(user_data)
    
    assert created_user.username == "alice"
    assert created_user.email == "alice@example.com"
    assert created_user.id is not None
    assert created_user.password_hash != "securepassword123"  # Password should be hashed


@pytest.mark.asyncio
async def test_register_user_duplicate_username():
    """Test registration with duplicate username."""
    repo = MockUserRepository()
    service = UserService(repo)

    # Create first user
    user_data = UserCreate(
        username="alice",
        email="alice@example.com",
        password="password123"
    )
    await service.register_user(user_data)

    # Try to create user with same username
    duplicate_user_data = UserCreate(
        username="alice",
        email="different@example.com",
        password="password456"
    )

    with pytest.raises(ConflictError, match="Username already taken"):
        await service.register_user(duplicate_user_data)


@pytest.mark.asyncio
async def test_register_user_duplicate_email():
    """Test registration with duplicate email."""
    repo = MockUserRepository()
    service = UserService(repo)

    # Create first user
    user_data = UserCreate(
        username="alice",
        email="alice@example.com",
        password="password123"
    )
    await service.register_user(user_data)

    # Try to create user with same email
    duplicate_user_data = UserCreate(
        username="bob",
        email="alice@example.com",
        password="password456"
    )

    with pytest.raises(ConflictError, match="Email already registered"):
        await service.register_user(duplicate_user_data)


@pytest.mark.asyncio
async def test_authenticate_user_success():
    """Test successful authentication."""
    repo = MockUserRepository()
    service = UserService(repo)

    # Register user first
    user_data = UserCreate(
        username="alice",
        email="alice@example.com",
        password="correctpassword"
    )
    await service.register_user(user_data)

    # Authenticate with correct credentials
    token = await service.authenticate_user("alice", "correctpassword")
    assert isinstance(token, str)
    assert len(token) > 0


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password():
    """Test authentication with wrong password."""
    repo = MockUserRepository()
    service = UserService(repo)

    # Register user first
    user_data = UserCreate(
        username="alice",
        email="alice@example.com",
        password="correctpassword"
    )
    await service.register_user(user_data)

    # Try to authenticate with wrong password
    with pytest.raises(AuthenticationError, match="Invalid credentials"):
        await service.authenticate_user("alice", "wrongpassword")


@pytest.mark.asyncio
async def test_authenticate_user_not_found():
    """Test authentication with non-existent user."""
    repo = MockUserRepository()
    service = UserService(repo)

    # Try to authenticate non-existent user
    with pytest.raises(AuthenticationError, match="Invalid credentials"):
        await service.authenticate_user("nonexistent", "anypassword")
