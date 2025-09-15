from fastapi import APIRouter, Depends, HTTPException, status
from app.domain.schemas.user_schema import UserCreate, UserResponse, Token, UserLogin
from app.application.services.user_service import UserService
from app.application.exceptions import AuthenticationError, ConflictError
from app.presentation.dependencies import get_user_service

router = APIRouter()

@router.get("/", response_model=dict)
async def auth_info():
    """Información sobre los endpoints de autenticación disponibles"""
    return {
        "message": "API de Autenticación - Prueba Técnica GPS Control",
        "version": "1.0.0",
        "endpoints": {
            "register": "POST /api/v1/auth/register",
            "login": "POST /api/v1/auth/login"
        },
        "documentation": "/docs"
    }

@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        user = await service.register_user(user_in)
        return user
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.post("/login", response_model=Token)
async def login(
    user_data: UserLogin,
    user_service: UserService = Depends(get_user_service)
):
    """
    Espera JSON { "username": "...", "password": "..." }.
    Devuelve: { "access_token": "...", "token_type": "bearer" }.
    """
    try:
        token = await user_service.authenticate_user(user_data.username, user_data.password)
        return {"access_token": token, "token_type": "bearer"}
    except AuthenticationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        # Log del error para debugging
        print(f"Unexpected error in login: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
