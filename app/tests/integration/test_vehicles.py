import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_vehicle_success(test_client: AsyncClient, test_user_token: str):
    """Test successful vehicle creation."""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    vehicle_data = {
        "brand": "Toyota",
        "arrival_location": "Bogotá",
        "applicant": "Juan Pérez"
    }

    response = await test_client.post("/api/v1/vehicles/", json=vehicle_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["brand"] == "Toyota"
    assert data["arrival_location"] == "Bogotá"
    assert data["applicant"] == "Juan Pérez"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_vehicle_unauthorized(test_client: AsyncClient):
    """Test vehicle creation without authentication."""
    vehicle_data = {
        "brand": "Toyota",
        "arrival_location": "Bogotá",
        "applicant": "Juan Pérez"
    }

    response = await test_client.post("/api/v1/vehicles/", json=vehicle_data)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_vehicle_invalid_data(test_client: AsyncClient, test_user_token: str):
    """Test vehicle creation with invalid data."""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    
    # Missing required fields
    response = await test_client.post("/api/v1/vehicles/", json={}, headers=headers)
    assert response.status_code == 422

    # Empty brand
    invalid_data = {
        "brand": "",
        "arrival_location": "Bogotá",
        "applicant": "Juan Pérez"
    }
    response = await test_client.post("/api/v1/vehicles/", json=invalid_data, headers=headers)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_vehicle_success(test_client: AsyncClient, test_user_token: str):
    """Test getting vehicle by ID."""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    
    # Create vehicle first
    vehicle_data = {
        "brand": "Honda",
        "arrival_location": "Medellín",
        "applicant": "Ana García"
    }
    create_response = await test_client.post("/api/v1/vehicles/", json=vehicle_data, headers=headers)
    assert create_response.status_code == 200
    created_vehicle = create_response.json()
    vehicle_id = created_vehicle["id"]

    # Get vehicle by ID
    response = await test_client.get(f"/api/v1/vehicles/{vehicle_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == vehicle_id
    assert data["brand"] == "Honda"
    assert data["applicant"] == "Ana García"


@pytest.mark.asyncio
async def test_get_vehicle_not_found(test_client: AsyncClient):
    """Test getting non-existent vehicle."""
    fake_id = "550e8400-e29b-41d4-a716-446655440999"
    response = await test_client.get(f"/api/v1/vehicles/{fake_id}")
    
    assert response.status_code == 404
    assert "Vehicle not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_list_vehicles_success(test_client: AsyncClient, test_user_token: str):
    """Test listing vehicles."""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    
    # Create multiple vehicles
    vehicles_data = [
        {"brand": "Toyota", "arrival_location": "Bogotá", "applicant": "Juan"},
        {"brand": "Honda", "arrival_location": "Medellín", "applicant": "Ana"},
        {"brand": "Ford", "arrival_location": "Cali", "applicant": "Carlos"}
    ]

    for vehicle_data in vehicles_data:
        create_response = await test_client.post("/api/v1/vehicles/", json=vehicle_data, headers=headers)
        assert create_response.status_code == 200

    # List vehicles
    response = await test_client.get("/api/v1/vehicles/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3  # At least the 3 we created


@pytest.mark.asyncio
async def test_update_vehicle_success(test_client: AsyncClient, test_user_token: str):
    """Test successful vehicle update."""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    
    # Create vehicle first
    vehicle_data = {
        "brand": "Toyota",
        "arrival_location": "Bogotá",
        "applicant": "Juan Pérez"
    }
    create_response = await test_client.post("/api/v1/vehicles/", json=vehicle_data, headers=headers)
    assert create_response.status_code == 200
    created_vehicle = create_response.json()
    vehicle_id = created_vehicle["id"]

    # Update vehicle
    update_data = {
        "brand": "Mazda",
        "arrival_location": "Medellín",
        "applicant": "María González"
    }
    response = await test_client.put(f"/api/v1/vehicles/{vehicle_id}", json=update_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == vehicle_id
    assert data["brand"] == "Mazda"
    assert data["arrival_location"] == "Medellín"
    assert data["applicant"] == "María González"


@pytest.mark.asyncio
async def test_update_vehicle_unauthorized(test_client: AsyncClient, test_user_token: str):
    """Test vehicle update without authentication."""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    
    # Create vehicle first
    vehicle_data = {
        "brand": "Toyota",
        "arrival_location": "Bogotá",
        "applicant": "Juan Pérez"
    }
    create_response = await test_client.post("/api/v1/vehicles/", json=vehicle_data, headers=headers)
    assert create_response.status_code == 200
    created_vehicle = create_response.json()
    vehicle_id = created_vehicle["id"]

    # Try to update without authorization
    update_data = {
        "brand": "Mazda",
        "arrival_location": "Medellín",
        "applicant": "María González"
    }
    response = await test_client.put(f"/api/v1/vehicles/{vehicle_id}", json=update_data)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_vehicle_not_found(test_client: AsyncClient, test_user_token: str):
    """Test updating non-existent vehicle."""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    
    fake_id = "550e8400-e29b-41d4-a716-446655440999"
    update_data = {
        "brand": "Mazda",
        "arrival_location": "Medellín",
        "applicant": "María González"
    }
    response = await test_client.put(f"/api/v1/vehicles/{fake_id}", json=update_data, headers=headers)
    
    assert response.status_code == 404
    assert "Vehicle not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_delete_vehicle_success(test_client: AsyncClient, test_user_token: str):
    """Test successful vehicle deletion."""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    
    # Create vehicle first
    vehicle_data = {
        "brand": "Toyota",
        "arrival_location": "Bogotá",
        "applicant": "Juan Pérez"
    }
    create_response = await test_client.post("/api/v1/vehicles/", json=vehicle_data, headers=headers)
    assert create_response.status_code == 200
    created_vehicle = create_response.json()
    vehicle_id = created_vehicle["id"]

    # Delete vehicle
    response = await test_client.delete(f"/api/v1/vehicles/{vehicle_id}", headers=headers)
    
    assert response.status_code == 200
    assert response.json()["detail"] == "deleted"

    # Verify vehicle is deleted
    get_response = await test_client.get(f"/api/v1/vehicles/{vehicle_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_vehicle_unauthorized(test_client: AsyncClient, test_user_token: str):
    """Test vehicle deletion without authentication."""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    
    # Create vehicle first
    vehicle_data = {
        "brand": "Toyota",
        "arrival_location": "Bogotá",
        "applicant": "Juan Pérez"
    }
    create_response = await test_client.post("/api/v1/vehicles/", json=vehicle_data, headers=headers)
    assert create_response.status_code == 200
    created_vehicle = create_response.json()
    vehicle_id = created_vehicle["id"]

    # Try to delete without authorization
    response = await test_client.delete(f"/api/v1/vehicles/{vehicle_id}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_vehicle_not_found(test_client: AsyncClient, test_user_token: str):
    """Test deleting non-existent vehicle."""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    
    fake_id = "550e8400-e29b-41d4-a716-446655440999"
    response = await test_client.delete(f"/api/v1/vehicles/{fake_id}", headers=headers)
    
    assert response.status_code == 404
    assert "Vehicle not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_complete_vehicle_crud_flow(test_client: AsyncClient, test_user_token: str):
    """Test complete CRUD flow for vehicles."""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    
    # 1. Create vehicle
    vehicle_data = {
        "brand": "Nissan",
        "arrival_location": "Cartagena",
        "applicant": "Pedro Martínez"
    }
    create_response = await test_client.post("/api/v1/vehicles/", json=vehicle_data, headers=headers)
    assert create_response.status_code == 200
    created_vehicle = create_response.json()
    vehicle_id = created_vehicle["id"]

    # 2. Read vehicle
    get_response = await test_client.get(f"/api/v1/vehicles/{vehicle_id}")
    assert get_response.status_code == 200
    assert get_response.json()["brand"] == "Nissan"

    # 3. Update vehicle
    update_data = {
        "brand": "Chevrolet",
        "arrival_location": "Barranquilla",
        "applicant": "Luisa Fernández"
    }
    update_response = await test_client.put(f"/api/v1/vehicles/{vehicle_id}", json=update_data, headers=headers)
    assert update_response.status_code == 200
    assert update_response.json()["brand"] == "Chevrolet"

    # 4. Delete vehicle
    delete_response = await test_client.delete(f"/api/v1/vehicles/{vehicle_id}", headers=headers)
    assert delete_response.status_code == 200

    # 5. Verify deletion
    final_get_response = await test_client.get(f"/api/v1/vehicles/{vehicle_id}")
    assert final_get_response.status_code == 404
