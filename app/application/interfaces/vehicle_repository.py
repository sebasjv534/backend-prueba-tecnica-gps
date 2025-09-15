from app.domain.models.vehicle_model import Vehicle

class IVehicleRepository:
    async def list(self, limit: int = 10, offset: int = 0) -> list[Vehicle]:
        raise NotImplementedError

    async def get_by_id(self, vehicle_id: str) -> Vehicle | None:
        raise NotImplementedError

    async def create(self, vehicle: Vehicle) -> Vehicle:
        raise NotImplementedError

    async def update(self, vehicle: Vehicle) -> Vehicle:
        raise NotImplementedError

    async def delete(self, vehicle_id: str) -> None:
        raise NotImplementedError
