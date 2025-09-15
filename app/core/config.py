from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Project Configuration
    PROJECT_NAME: str = "Prueba Tecnica GPSCONTROL"
    VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False)
    
    # Database Configuration
    DATABASE_URL: str = Field(..., description="Database connection URL")
    
    # JWT Configuration
    JWT_SECRET: str = Field(..., min_length=32, description="JWT secret key")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_EXPIRATION_MINUTES: int = Field(default=60, ge=1, le=10080, description="JWT expiration in minutes")
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )
    
    # Server Configuration
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, ge=1, le=65535, description="Server port")
    
    # Environment
    ENVIRONMENT: str = Field(default="development", pattern="^(development|staging|production)$")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "validate_assignment": True
    }

    @field_validator("DATABASE_URL")
    def validate_database_url(cls, v):
        # Aceptar múltiples formatos de URLs de PostgreSQL
        valid_prefixes = (
            "postgresql://", 
            "postgresql+asyncpg://", 
            "postgresql+psycopg://",
            "postgresql+psycopg2://",
            "sqlite://", 
            "mysql://"
        )
        if not v.startswith(valid_prefixes):
            raise ValueError("DATABASE_URL must be a valid database URL")
        return v

    @field_validator("JWT_SECRET")
    def validate_jwt_secret(cls, v):
        if len(v) < 32:
            raise ValueError("JWT_SECRET must be at least 32 characters long")
        return v


settings = Settings()