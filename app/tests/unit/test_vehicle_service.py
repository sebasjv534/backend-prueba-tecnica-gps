import pytest
from unittest.mock import Mock, AsyncMock
from uuid import UUID
from datetime import datetime

from app.application.services.vehicle_service import VehicleService
from app.domain.schemas.vehicle_schema import VehicleCreate
from app.application.exceptions import NotFoundError
from app.domain.models.vehicle_model import Vehicle


class MockVehicleRepository:
    def __init__(self):
        self._vehicles = {}
        self._counter = 1

    async def list(self, limit: int = 10, offset: int = 0):
        vehicles = list(self._vehicles.values())
        return vehicles[offset:offset + limit]

    async def create(self, vehicle: Vehicle):
        # Simular creación con ID
        vehicle.id = f"550e8400-e29b-41d4-a716-44665544000{self._counter}"
        vehicle.created_at = datetime.utcnow()
        vehicle.updated_at = datetime.utcnow()
        
        self._vehicles[vehicle.id] = vehicle
        self._counter += 1
        return vehicle

    async def get_by_id(self, vehicle_id: str):
        return self._vehicles.get(vehicle_id)

    async def update(self, vehicle: Vehicle):
        if vehicle.id in self._vehicles:
            vehicle.updated_at = datetime.utcnow()
            self._vehicles[vehicle.id] = vehicle
            return vehicle
        return None

    async def delete(self, vehicle_id: str):
        self._vehicles.pop(vehicle_id, None)


@pytest.mark.asyncio
async def test_create_vehicle_success():
    """Test successful vehicle creation."""
    repo = MockVehicleRepository()
    service = VehicleService(repo)

    vehicle_data = VehicleCreate(
        brand="Toyota",
        arrival_location="Bogotá",
        applicant="Juan Pérez"
    )

    created_vehicle = await service.create_vehicle(vehicle_data)
    
    assert created_vehicle.brand == "Toyota"
    assert created_vehicle.arrival_location == "Bogotá"
    assert created_vehicle.applicant == "Juan Pérez"
    assert created_vehicle.id is not None
    assert created_vehicle.created_at is not None


@pytest.mark.asyncio
async def test_get_vehicle_success():
    """Test getting vehicle by ID."""
    repo = MockVehicleRepository()
    service = VehicleService(repo)

    # Create vehicle first
    vehicle_data = VehicleCreate(
        brand="Honda",
        arrival_location="Medellín",
        applicant="Ana García"
    )
    created_vehicle = await service.create_vehicle(vehicle_data)

    # Get vehicle by ID
    found_vehicle = await service.get_vehicle(created_vehicle.id)
    assert found_vehicle is not None
    assert found_vehicle.brand == "Honda"
    assert found_vehicle.applicant == "Ana García"


@pytest.mark.asyncio
async def test_get_vehicle_not_found():
    """Test getting non-existent vehicle."""
    repo = MockVehicleRepository()
    service = VehicleService(repo)

    with pytest.raises(NotFoundError, match="Vehicle not found"):
        await service.get_vehicle("550e8400-e29b-41d4-a716-446655440999")


@pytest.mark.asyncio
async def test_list_vehicles():
    """Test listing vehicles with pagination."""
    repo = MockVehicleRepository()
    service = VehicleService(repo)

    # Create multiple vehicles
    vehicles_data = [
        VehicleCreate(brand="Toyota", arrival_location="Bogotá", applicant="Juan"),
        VehicleCreate(brand="Honda", arrival_location="Medellín", applicant="Ana"),
        VehicleCreate(brand="Ford", arrival_location="Cali", applicant="Carlos")
    ]

    for vehicle_data in vehicles_data:
        await service.create_vehicle(vehicle_data)

    # List all vehicles
    vehicles = await service.list_vehicles()
    assert len(vehicles) == 3

    # List with limit
    vehicles_limited = await service.list_vehicles(limit=2)
    assert len(vehicles_limited) == 2

    # List with offset
    vehicles_offset = await service.list_vehicles(limit=2, offset=1)
    assert len(vehicles_offset) == 2


@pytest.mark.asyncio
async def test_update_vehicle_success():
    """Test successful vehicle update."""
    repo = MockVehicleRepository()
    service = VehicleService(repo)

    # Create vehicle first
    vehicle_data = VehicleCreate(
        brand="Toyota",
        arrival_location="Bogotá",
        applicant="Juan Pérez"
    )
    created_vehicle = await service.create_vehicle(vehicle_data)

    # Update vehicle
    update_data = VehicleCreate(
        brand="Mazda",
        arrival_location="Medellín",
        applicant="María González"
    )

    updated_vehicle = await service.update_vehicle(created_vehicle.id, update_data)
    
    assert updated_vehicle.brand == "Mazda"
    assert updated_vehicle.arrival_location == "Medellín"
    assert updated_vehicle.applicant == "María González"
    assert updated_vehicle.id == created_vehicle.id
    assert updated_vehicle.updated_at is not None


@pytest.mark.asyncio
async def test_update_vehicle_not_found():
    """Test updating non-existent vehicle."""
    repo = MockVehicleRepository()
    service = VehicleService(repo)

    update_data = VehicleCreate(
        brand="Mazda",
        arrival_location="Medellín",
        applicant="María González"
    )

    with pytest.raises(NotFoundError, match="Vehicle not found"):
        await service.update_vehicle("550e8400-e29b-41d4-a716-446655440999", update_data)


@pytest.mark.asyncio
async def test_delete_vehicle_success():
    """Test successful vehicle deletion."""
    repo = MockVehicleRepository()
    service = VehicleService(repo)

    # Create vehicle first
    vehicle_data = VehicleCreate(
        brand="Toyota",
        arrival_location="Bogotá",
        applicant="Juan Pérez"
    )
    created_vehicle = await service.create_vehicle(vehicle_data)

    # Delete vehicle
    await service.delete_vehicle(created_vehicle.id)

    # Verify vehicle is deleted
    with pytest.raises(NotFoundError, match="Vehicle not found"):
        await service.get_vehicle(created_vehicle.id)


@pytest.mark.asyncio
async def test_delete_vehicle_not_found():
    """Test deleting non-existent vehicle."""
    repo = MockVehicleRepository()
    service = VehicleService(repo)

    with pytest.raises(NotFoundError, match="Vehicle not found"):
        await service.delete_vehicle("550e8400-e29b-41d4-a716-446655440999")
