class AppError(Exception):
    """Excepción base de la aplicación."""
    def __init__(self, message: str, code: str = "app_error"):
        super().__init__(message)
        self.code = code
        self.message = message

class NotFoundError(AppError):
    """Recurso no encontrado (404)."""
    def __init__(self, message="Not found"):
        super().__init__(message, code="not_found")

class ConflictError(AppError):
    """Conflicto (409)."""
    def __init__(self, message="Conflict"):
        super().__init__(message, code="conflict")

class ValidationError(AppError):
    """Error de validación (400)."""
    def __init__(self, message="Validation error"):
        super().__init__(message, code="validation_error")

class AuthenticationError(AppError):
    """Error de autenticación (401)."""
    def __init__(self, message="Invalid credentials"):
        super().__init__(message, code="auth_error")
