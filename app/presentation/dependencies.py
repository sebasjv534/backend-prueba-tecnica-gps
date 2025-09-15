from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.infrastructure.repositories.user_repository import UserRepositorySQLAlchemy
from app.application.services.user_service import UserService
from app.application.exceptions import AuthenticationError
from app.infrastructure.repositories.vehicle_repository import VehicleRepositorySQLAlchemy
from app.application.services.vehicle_service import VehicleService
from app.core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepositorySQLAlchemy:
    return UserRepositorySQLAlchemy(db)

async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    repo = UserRepositorySQLAlchemy(db)
    return UserService(repo)

async def get_current_user(token: str = Depends(oauth2_scheme), user_service: UserService = Depends(get_user_service)):
    """
    Valida el JWT (usando oauth2_scheme), extrae el "sub" y devuelve el User.
    Lanza HTTP 401 si el token no es válido o el usuario no existe.
    """
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = await user_service.user_repo.get_by_id(user_id)  # direct access to repo (fast)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

async def get_vehicle_service(db: AsyncSession = Depends(get_db)) -> VehicleService:
    repo = VehicleRepositorySQLAlchemy(db)
    return VehicleService(repo)
