import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user_success(test_client: AsyncClient):
    """Test successful user registration."""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "securepassword123"
    }

    response = await test_client.post("/api/v1/auth/register", json=user_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "password" not in data  # Password should not be returned


@pytest.mark.asyncio
async def test_register_user_duplicate_username(test_client: AsyncClient):
    """Test registration with duplicate username."""
    user_data = {
        "username": "duplicateuser",
        "email": "user1@example.com",
        "password": "password123"
    }

    # First registration
    response1 = await test_client.post("/api/v1/auth/register", json=user_data)
    assert response1.status_code == 200

    # Second registration with same username
    user_data2 = {
        "username": "duplicateuser",
        "email": "user2@example.com", 
        "password": "password456"
    }

    response2 = await test_client.post("/api/v1/auth/register", json=user_data2)
    assert response2.status_code == 409
    assert "Username already taken" in response2.json()["detail"]


@pytest.mark.asyncio
async def test_register_user_duplicate_email(test_client: AsyncClient):
    """Test registration with duplicate email."""
    user_data = {
        "username": "user1",
        "email": "duplicate@example.com",
        "password": "password123"
    }

    # First registration
    response1 = await test_client.post("/api/v1/auth/register", json=user_data)
    assert response1.status_code == 200

    # Second registration with same email
    user_data2 = {
        "username": "user2",
        "email": "duplicate@example.com",
        "password": "password456"
    }

    response2 = await test_client.post("/api/v1/auth/register", json=user_data2)
    assert response2.status_code == 409
    assert "Email already registered" in response2.json()["detail"]


@pytest.mark.asyncio
async def test_register_user_invalid_data(test_client: AsyncClient):
    """Test registration with invalid data."""
    # Missing required fields
    response = await test_client.post("/api/v1/auth/register", json={})
    assert response.status_code == 422

    # Invalid email format
    invalid_data = {
        "username": "testuser",
        "email": "invalid-email",
        "password": "password123"
    }
    response = await test_client.post("/api/v1/auth/register", json=invalid_data)
    assert response.status_code == 422

    # Password too short
    short_password_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "123"
    }
    response = await test_client.post("/api/v1/auth/register", json=short_password_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_user_success(test_client: AsyncClient):
    """Test successful user login."""
    # Register user first
    user_data = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "loginpassword123"
    }
    register_response = await test_client.post("/api/v1/auth/register", json=user_data)
    assert register_response.status_code == 200

    # Login
    login_data = {
        "username": "loginuser",
        "password": "loginpassword123"
    }
    response = await test_client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0


@pytest.mark.asyncio
async def test_login_user_wrong_password(test_client: AsyncClient):
    """Test login with wrong password."""
    # Register user first
    user_data = {
        "username": "wrongpassuser",
        "email": "wrongpass@example.com",
        "password": "correctpassword"
    }
    register_response = await test_client.post("/api/v1/auth/register", json=user_data)
    assert register_response.status_code == 200

    # Login with wrong password
    login_data = {
        "username": "wrongpassuser",
        "password": "wrongpassword"
    }
    response = await test_client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_user_not_found(test_client: AsyncClient):
    """Test login with non-existent user."""
    login_data = {
        "username": "nonexistentuser",
        "password": "anypassword"
    }
    response = await test_client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_user_invalid_data(test_client: AsyncClient):
    """Test login with invalid data."""
    # Missing required fields
    response = await test_client.post("/api/v1/auth/login", json={})
    assert response.status_code == 422

    # Missing password
    response = await test_client.post("/api/v1/auth/login", json={"username": "test"})
    assert response.status_code == 422

    # Missing username
    response = await test_client.post("/api/v1/auth/login", json={"password": "test"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_full_auth_flow(test_client: AsyncClient):
    """Test complete authentication flow: register -> login -> use token."""
    # Register
    user_data = {
        "username": "flowuser",
        "email": "flow@example.com",
        "password": "flowpassword123"
    }
    
    register_response = await test_client.post("/api/v1/auth/register", json=user_data)
    assert register_response.status_code == 200
    user = register_response.json()
    
    # Login
    login_data = {
        "username": "flowuser",
        "password": "flowpassword123"
    }
    
    login_response = await test_client.post("/api/v1/auth/login", json=login_data)
    assert login_response.status_code == 200
    token_data = login_response.json()
    
    # Use token to access protected endpoint (vehicles)
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    vehicles_response = await test_client.get("/api/v1/vehicles/", headers=headers)
    assert vehicles_response.status_code == 200
