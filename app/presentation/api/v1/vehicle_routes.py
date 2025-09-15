from fastapi import APIRouter, Depends, HTTPException, status
from app.domain.schemas.vehicle_schema import VehicleCreate, VehicleResponse
from app.application.services.vehicle_service import VehicleService
from app.application.exceptions import NotFoundError
from app.presentation.dependencies import get_vehicle_service, get_current_user

router = APIRouter()

@router.get("/", response_model=list[VehicleResponse])
async def list_vehicles(service: VehicleService = Depends(get_vehicle_service)):
    return await service.list_vehicles()

@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(vehicle_id: str, service: VehicleService = Depends(get_vehicle_service)):
    try:
        return await service.get_vehicle(vehicle_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=VehicleResponse)
async def create_vehicle(vehicle: VehicleCreate, 
                         service: VehicleService = Depends(get_vehicle_service),
                         current_user = Depends(get_current_user)):
    return await service.create_vehicle(vehicle)

@router.put("/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(vehicle_id: str, vehicle: VehicleCreate, 
                         service: VehicleService = Depends(get_vehicle_service),
                         current_user = Depends(get_current_user)):
    try:
        return await service.update_vehicle(vehicle_id, vehicle)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{vehicle_id}")
async def delete_vehicle(vehicle_id: str, 
                         service: VehicleService = Depends(get_vehicle_service),
                         current_user = Depends(get_current_user)):
    try:
        await service.delete_vehicle(vehicle_id)
        return {"detail": "deleted"}
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
