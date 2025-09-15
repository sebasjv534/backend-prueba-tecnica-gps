from pydantic import BaseModel, EmailStr, ConfigDict, field_serializer, field_validator
from datetime import datetime
from uuid import UUID

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return v.strip()
    
    @field_validator('password')
    @classmethod  
    def validate_password(cls, v):
        if not v or len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class UserLogin(BaseModel): 
    username: str
    password: str

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    created_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
    
    @field_serializer('id')
    def serialize_id(self, value: UUID) -> str:
        """Convertir UUID a string para JSON"""
        return str(value)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
