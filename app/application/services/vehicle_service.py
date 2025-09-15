from app.application.interfaces.vehicle_repository import IVehicleRepository
from app.domain.schemas.vehicle_schema import VehicleCreate
from app.domain.models.vehicle_model import Vehicle
from app.application.exceptions import NotFoundError

class VehicleService:
   
    def __init__(self, vehicle_repo: IVehicleRepository):
        self.vehicle_repo = vehicle_repo

    async def list_vehicles(self, limit: int = 10, offset: int = 0) -> list[Vehicle]:
        return await self.vehicle_repo.list(limit=limit, offset=offset)

    async def create_vehicle(self, vehicle_in: VehicleCreate) -> Vehicle:
        """
        Crea un Vehicle a partir del DTO VehicleCreate.
        Convierte el DTO a la entidad (SQLAlchemy) antes de llamar al repo.
        """
        vehicle = Vehicle(**vehicle_in.model_dump())
        created = await self.vehicle_repo.create(vehicle)
        return created

    async def get_vehicle(self, vehicle_id: str) -> Vehicle:
        v = await self.vehicle_repo.get_by_id(vehicle_id)
        if not v:
            raise NotFoundError("Vehicle not found")
        return v

    async def update_vehicle(self, vehicle_id: str, vehicle_in: VehicleCreate) -> Vehicle:
        """
        Modelo simple de actualización:
        - busca entidad existente
        - actualiza atributos permitidos
        - delega al repo para persistir
        """
        existing = await self.vehicle_repo.get_by_id(vehicle_id)
        if not existing:
            raise NotFoundError("Vehicle not found")
        for k, val in vehicle_in.model_dump().items():
            setattr(existing, k, val)
        updated = await self.vehicle_repo.update(existing)
        return updated

    async def delete_vehicle(self, vehicle_id: str) -> None:
        existing = await self.vehicle_repo.get_by_id(vehicle_id)
        if not existing:
            raise NotFoundError("Vehicle not found")
        await self.vehicle_repo.delete(vehicle_id)
