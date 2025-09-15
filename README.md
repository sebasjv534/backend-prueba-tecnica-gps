# 🚗 Backend Prueba Técnica GPS Control

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-36%20passing-brightgreen.svg)](tests)

## 📋 Descripción

API REST backend desarrollada con **FastAPI** para el sistema de gestión de vehículos GPS Control. Implementa una arquitectura limpia (Clean Architecture) con patrones de diseño robustos, autenticación JWT y testing completo.

### ✨ Características Principales

- 🏗️ **Clean Architecture** - Separación clara de responsabilidades
- 🔐 **Autenticación JWT** - Sistema seguro con bcrypt
- 📊 **Base de datos async** - PostgreSQL con SQLAlchemy 2.0
- 🧪 **Testing completo** - 36 pruebas (unitarias e integración)
- 📝 **Documentación automática** - Swagger/OpenAPI
- 🚀 **Deploy en Render** - Configuración lista para producción
- 🔄 **WebSockets** - Comunicación en tiempo real
- ✅ **Validación robusta** - Pydantic v2 schemas

---

## Objetivo

El propósito principal de esta API es demostrar **buenas prácticas de arquitectura de software** en un escenario realista.  
La aplicación busca destacar no solo por cumplir los requisitos funcionales, sino también por su **estructura modular, seguridad integrada, pruebas automatizadas y despliegue en la nube**.

## 🛠️ Stack Tecnológico

| Categoría | Tecnología | Justificación |
|-----------|------------|---------------|
| **Framework** | FastAPI 0.104+ | Rendimiento ASGI, validación automática, docs interactiva |
| **Lenguaje** | Python 3.11+ | Tipado estático, async/await nativo, ecosistema maduro |
| **Base de datos** | PostgreSQL 15+ | Motor SQL robusto, escalable, compatible con Render |
| **ORM** | SQLAlchemy 2.0 (async) | Control total de queries, soporte async/await |
| **Autenticación** | JWT + bcrypt | Estándar moderno, seguro y portable |
| **Testing** | pytest + pytest-asyncio | Pruebas unitarias e integración fáciles |
| **Deploy** | Render | Integración GitHub, soporte Python/PostgreSQL |
| **Validación** | Pydantic v2 | Validación robusta con Python typing |

## 🏗️ Arquitectura (Clean Architecture)

```
app/
├── core/                 # Configuración y utilidades
│   ├── config.py        # Variables de entorno
│   ├── database.py      # Conexión DB async
│   └── security.py      # JWT y hashing
├── domain/              # Entidades de negocio
│   ├── models/          # Modelos SQLAlchemy
│   └── schemas/         # Schemas Pydantic
├── application/         # Lógica de negocio
│   ├── services/        # Servicios de aplicación
│   ├── interfaces/      # Contratos de repositorios
│   └── exceptions.py    # Excepciones personalizadas
├── infrastructure/      # Capa de datos
│   └── repositories/    # Implementaciones de repositorios
├── presentation/        # Capa de presentación
│   ├── api/v1/         # Endpoints REST
│   └── dependencies.py # Inyección de dependencias
├── websocket/          # WebSockets en tiempo real
└── tests/              # Suite de pruebas
    ├── unit/           # Pruebas unitarias (14)
    └── integration/    # Pruebas de integración (22)
```

**Decisión técnica:** se adopta **Clean Architecture** para separar responsabilidades:  
- **Domain** → qué hace el sistema (entidades, modelos, reglas)
- **Application** → cómo lo hace (casos de uso)
- **Infrastructure** → con qué lo hace (PostgreSQL, repositorios)
- **Presentation** → cómo se expone al exterior (API REST)

Esto permite **alta mantenibilidad, facilidad de pruebas y escalabilidad**.

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.11+
- PostgreSQL 15+
- Git

### Configuración Local

1. **Clonar el repositorio**
```bash
git clone https://github.com/sebasjv534/backend-prueba-tecnica-gps.git
cd backend-prueba-tecnica-gps
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
```

Editar `.env` con tus configuraciones:
```env
PROJECT_NAME=Vehicle API
DEBUG=true
ENVIRONMENT=development
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/vehicles
JWT_SECRET=tu_jwt_secret_de_32_caracteres_minimo
JWT_EXPIRATION_MINUTES=60
```

5. **Ejecutar la aplicación**
```bash
uvicorn app.main:app --reload
```

La API estará disponible en: `http://localhost:8000`

## 📚 Documentación de la API

Una vez ejecutada la aplicación, puedes acceder a:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## 🔐 Endpoints Principales

### Autenticación
- `POST /api/v1/auth/register` - Registro de usuario
- `POST /api/v1/auth/login` - Inicio de sesión

### Vehículos (requiere autenticación)
- `GET /api/v1/vehicles/` - Listar vehículos
- `POST /api/v1/vehicles/` - Crear vehículo
- `GET /api/v1/vehicles/{id}` - Obtener vehículo
- `PUT /api/v1/vehicles/{id}` - Actualizar vehículo
- `DELETE /api/v1/vehicles/{id}` - Eliminar vehículo

### Utilidades
- `GET /health` - Health check

## 🧪 Testing

El proyecto cuenta con una suite completa de **36 pruebas**:

```bash
# Ejecutar todas las pruebas
pytest

# Solo pruebas unitarias (14)
pytest app/tests/unit/ -v

# Solo pruebas de integración (22)
pytest app/tests/integration/ -v

# Con coverage
pytest --cov=app --cov-report=html
```

### Cobertura de Pruebas

- ✅ **Servicios de usuario**: Registro, autenticación, validaciones
- ✅ **Servicios de vehículo**: CRUD completo, casos de error
- ✅ **Endpoints de autenticación**: E2E con JWT
- ✅ **Endpoints de vehículos**: CRUD completo E2E
- ✅ **Manejo de errores**: Códigos HTTP correctos
- ✅ **Validaciones**: Datos inválidos y casos edge

## 🚀 Deploy en Render

El proyecto está configurado para desplegarse automáticamente en [Render](https://render.com).

### Configuración automática:

1. **Procfile** - Comando de inicio para Render
2. **requirements.txt** - Dependencias de Python
3. **Variables de entorno** - Configurar en Render dashboard

### Variables requeridas en Render:

```env
DATABASE_URL=postgresql://...
JWT_SECRET=tu_jwt_secret_seguro
ENVIRONMENT=production
```

## 🔄 WebSockets

La aplicación incluye soporte para WebSockets en tiempo real:

```javascript
// Conectar a WebSocket
const ws = new WebSocket('ws://localhost:8000/ws');
ws.onmessage = (event) => {
    console.log('Mensaje recibido:', JSON.parse(event.data));
};
```

## 🌟 Características Avanzadas

### Seguridad
- 🔐 Autenticación JWT con expiración configurable
- 🛡️ Hashing de contraseñas con bcrypt
- 🚫 Validación de entrada con Pydantic
- 🔒 Protección contra inyección SQL

### Performance
- ⚡ Operaciones de base de datos asíncronas
- 🗄️ Connection pooling con SQLAlchemy
- 📊 Paginación en listados
- 🎯 Queries optimizadas

### Monitoreo
- 📈 Health check endpoint
- 🐛 Logging estructurado
- 📊 Manejo centralizado de excepciones

## 🤝 Contribución

### Git Flow

Utilizamos Git Flow para el manejo de ramas:

```
main (producción)
├── develop (desarrollo)
│   ├── sebasdev (rama personal)
│   │   ├── feature/nueva-funcionalidad
│   │   ├── feature/testing
│   │   └── bugfix/correción
```

### Conventional Commits

Utilizamos conventional commits en español:

```bash
feat: nueva funcionalidad
fix: corrección de bug
test: añadir o corregir pruebas
docs: cambios en documentación
chore: tareas de mantenimiento
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 👥 Autor

**Sebastian Jiménez**
- GitHub: [@sebasjv534](https://github.com/sebasjv534)
- Email: sebastianjimenez534@gmail.com

---

⭐ Si este proyecto te resulta útil, ¡no olvides darle una estrella!


