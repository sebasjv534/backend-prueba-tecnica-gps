from pydantic import BaseModel, ConfigDict, field_serializer, field_validator
from datetime import datetime
from uuid import UUID

class VehicleCreate(BaseModel):
    brand: str
    arrival_location: str
    applicant: str
    
    @field_validator('brand')
    @classmethod
    def validate_brand(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Brand cannot be empty')
        return v.strip()
    
    @field_validator('arrival_location')
    @classmethod
    def validate_arrival_location(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Arrival location cannot be empty')
        return v.strip()
    
    @field_validator('applicant')
    @classmethod
    def validate_applicant(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Applicant cannot be empty')
        return v.strip()

class VehicleResponse(VehicleCreate):
    id: UUID  # Cambiar de str a UUID
    created_at: datetime | None
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
    
    @field_serializer('id')
    def serialize_id(self, value: UUID) -> str:
        """Convertir UUID a string para JSON"""
        return str(value)
