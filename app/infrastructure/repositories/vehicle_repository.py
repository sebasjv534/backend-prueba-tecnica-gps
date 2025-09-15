from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.domain.models.vehicle_model import Vehicle
from app.application.interfaces.vehicle_repository import IVehicleRepository

class VehicleRepositorySQLAlchemy(IVehicleRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self, limit: int = 10, offset: int = 0) -> list[Vehicle]:
        result = await self.db.execute(select(Vehicle).offset(offset).limit(limit))
        return result.scalars().all()

    async def get_by_id(self, vehicle_id: str) -> Vehicle | None:
        try:
            # Convertir string a UUID
            uuid_id = UUID(vehicle_id)
            result = await self.db.execute(select(Vehicle).where(Vehicle.id == uuid_id))
            return result.scalars().first()
        except ValueError:
            # Si el string no es un UUID válido, retornar None
            return None

    async def create(self, vehicle: Vehicle) -> Vehicle:
        self.db.add(vehicle)
        await self.db.commit()
        await self.db.refresh(vehicle)
        return vehicle

    async def update(self, vehicle: Vehicle) -> Vehicle:
        self.db.add(vehicle)
        await self.db.commit()
        await self.db.refresh(vehicle)
        return vehicle

    async def delete(self, vehicle_id: str) -> None:
        try:
            # Convertir string a UUID
            uuid_id = UUID(vehicle_id)
            result = await self.db.execute(select(Vehicle).where(Vehicle.id == uuid_id))
            vehicle = result.scalars().first()
            if vehicle:
                await self.db.delete(vehicle)
                await self.db.commit()
        except ValueError:
            # Si el string no es un UUID válido, no hacer nada
            pass
