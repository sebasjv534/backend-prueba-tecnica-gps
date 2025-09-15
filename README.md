# Backend API - Prueba Técnica

Este proyecto es un **backend desarrollado con FastAPI**, diseñado siguiendo los principios de **Clean Architecture**, **SOLID** y prácticas de seguridad basadas en **OWASP Top 10**.  
La API provee endpoints RESTful para la gestión de **usuarios** y **vehículos**, con autenticación y autorización implementadas mediante **JWT**.  

El objetivo es construir una aplicación **robusta, escalable y segura**, que pueda integrarse con un frontend moderno (Next.js).

---

## Objetivo

El propósito principal de esta API es demostrar **buenas prácticas de arquitectura de software** en un escenario realista.  
La aplicación busca destacar no solo por cumplir los requisitos funcionales, sino también por su **estructura modular, seguridad integrada, pruebas automatizadas y despliegue en la nube**.

---

## Stack Tecnológico

- **Lenguaje:** Python 3.11+
- **Framework principal:** [FastAPI](https://fastapi.tiangolo.com/)  
  ✔ Elección: por su rendimiento (ASGI), validación automática con Pydantic y documentación interactiva.
- **Base de Datos:** PostgreSQL  
  ✔ Elección: motor SQL robusto, escalable y compatible con Render (PaaS).
- **ORM:** SQLAlchemy (modo asíncrono)  
  ✔ Elección: control total sobre las queries, soporte de async/await.
- **Migraciones:** Alembic  
  ✔ Elección: versionado de base de datos confiable y estándar en proyectos profesionales.
- **Autenticación:** JWT con `python-jose` y `passlib[bcrypt]`  
  ✔ Elección: estándar en APIs modernas, seguro y portable.
- **Testing:** Pytest + HTTPX  
  ✔ Elección: pruebas unitarias y de integración fáciles de escribir y ejecutar.
- **Despliegue:** Render (PaaS)  
  ✔ Elección: simplicidad de integración con GitHub, soporte nativo para Python y PostgreSQL.
- **Estilo de código:** Black, Flake8, Isort  
  ✔ Elección: mantener un código limpio y consistente de forma automática.

---

## 📂 Estructura del Proyecto (Clean Architecture)

app/
├── application/ # Casos de uso (lógica de negocio)
├── core/ # Configuración, seguridad, conexión a BD
├── domain/ # Entidades y DTOs (schemas)
├── infrastructure/ # Implementaciones (repositorios, adaptadores)
├── presentation/ # API (routers, dependencias, validaciones)
├── main.py # Punto de entrada FastAPI


**Decisión técnica:** se adopta **Clean Architecture** para separar responsabilidades:  
- **Domain** → qué hace el sistema (entidades, modelos, reglas).  
- **Application** → cómo lo hace (casos de uso).  
- **Infrastructure** → con qué lo hace (PostgreSQL, repositorios).  
- **Presentation** → cómo se expone al exterior (API REST).  

Esto permite **alta mantenibilidad, facilidad de pruebas y escalabilidad**.


