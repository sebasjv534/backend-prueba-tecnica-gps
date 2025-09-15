import pytest
import pytest_asyncio
import asyncio
from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db, Base
from app.core.config import settings

# Base de datos de prueba en memoria
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True
    )
    
    # Crear todas las tablas
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Limpiar después de las pruebas
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()

@pytest_asyncio.fixture
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    TestSessionLocal = sessionmaker(
        test_engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
    
    async with TestSessionLocal() as session:
        yield session
        # No intentamos hacer rollback manual

@pytest_asyncio.fixture
async def test_client(test_session: AsyncSession):
    """Create test client with database session override."""
    async def override_get_db():
        yield test_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(base_url="http://test") as client:
        # Custom transport to work with FastAPI app
        from httpx import ASGITransport
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as test_client:
            yield test_client
    
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def test_user_token(test_client: AsyncClient) -> str:
    """Create a test user and return authentication token."""
    import time
    unique_suffix = str(int(time.time() * 1000))  # timestamp único
    
    # Registrar usuario de prueba con nombre único
    user_data = {
        "username": f"testuser_{unique_suffix}",
        "email": f"test_{unique_suffix}@example.com",
        "password": "testpassword123"
    }
    
    register_response = await test_client.post("/api/v1/auth/register", json=user_data)
    assert register_response.status_code == 200
    
    # Hacer login para obtener token
    login_data = {
        "username": f"testuser_{unique_suffix}",
        "password": "testpassword123"
    }
    
    login_response = await test_client.post("/api/v1/auth/login", json=login_data)
    assert login_response.status_code == 200
    
    token = login_response.json()["access_token"]
    return token