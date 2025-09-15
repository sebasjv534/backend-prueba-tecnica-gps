from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.presentation.api.v1 import auth_routes, vehicle_routes
from app.application.exceptions import AppError, NotFoundError, ConflictError, AuthenticationError

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API backend prueba técnica GPSCONTROL",
    version="1.0.0",
    lifespan=lifespan,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React development
        "http://localhost:3001",  # Backup local port
        "https://localhost:3000", # HTTPS local
        "https://tu-frontend-domain.com",  # Dominio de producción del frontend
        "*"  # Permitir todos los orígenes (solo para desarrollo - remover en producción)
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(vehicle_routes.router, prefix="/api/v1/vehicles", tags=["vehicles"])

@app.get("/", tags=["root"])
async def root():
    """Endpoint raíz de la API"""
    return {
        "message": "Prueba Técnica GPSCONTROL API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }

@app.get("/health", tags=["health"])
async def health_check():
    """Endpoint de verificación de salud"""
    return {
        "status": "ok",
        "version": "1.0.0",
        "database": "connected"
    }

# --- Global Exception Handlers ---
@app.exception_handler(NotFoundError)
async def not_found_error_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message}
    )

@app.exception_handler(ConflictError)
async def conflict_error_handler(request: Request, exc: ConflictError):
    return JSONResponse(
        status_code=409,
        content={"detail": exc.message}
    )

@app.exception_handler(AuthenticationError)
async def auth_error_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(
        status_code=401,
        content={"detail": exc.message}
    )

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    status_map = {
        "not_found": 404,
        "conflict": 409,
        "auth_error": 401,
    }
    status_code = status_map.get(exc.code, 400)
    return JSONResponse(
        status_code=status_code,
        content={"detail": exc.message}
    )