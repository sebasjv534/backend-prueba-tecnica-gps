from app.application.interfaces.user_repository import IUserRepository
from app.domain.schemas.user_schema import UserCreate
from app.domain.models.user_model import User
from app.core.security import hash_password, verify_password, create_access_token
from app.application.exceptions import ConflictError, AuthenticationError, NotFoundError
from sqlalchemy.exc import IntegrityError

class UserService:
    
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def register_user(self, user_in: UserCreate) -> User:
        """
        Registra un nuevo usuario:
         - valida unicidad por username y email (delegado al repo)
         - hashea la contraseña
         - crea y devuelve el user (modelo SQLAlchemy)
        """
        # Validar username único
        existing_user = await self.user_repo.get_by_username(user_in.username)
        if existing_user:
            raise ConflictError("Username already taken")
        
        # Validar email único
        existing_email = await self.user_repo.get_by_email(user_in.email)
        if existing_email:
            raise ConflictError("Email already registered")

        # Crear usuario
        hashed = hash_password(user_in.password)
        user = User(username=user_in.username, email=user_in.email, password_hash=hashed)
        
        try:
            created = await self.user_repo.create(user)
            return created
        except IntegrityError as e:
            # Manejo de errores de base de datos como backup
            if "users_email_key" in str(e):
                raise ConflictError("Email already registered")
            elif "ix_users_username" in str(e):
                raise ConflictError("Username already taken")
            else:
                raise ConflictError("User registration failed due to constraint violation")

    async def authenticate_user(self, username: str, password: str) -> str:
        """
        Autentica por username/password. Devuelve JWT string.
        Lanza AuthenticationError si falla.
        """
        print(f"Attempting to authenticate user: {username}")  # Debug log
        user = await self.user_repo.get_by_username(username)
        
        if not user:
            print(f"User not found: {username}")  # Debug log
            raise AuthenticationError("Invalid credentials")
            
        print(f"User found: {user.username}, checking password...")  # Debug log
        password_valid = verify_password(password, user.password_hash)
        print(f"Password valid: {password_valid}")  # Debug log
        
        if not password_valid:
            raise AuthenticationError("Invalid credentials")
            
        token = create_access_token(subject=str(user.id))
        print(f"Token created successfully for user: {username}")  # Debug log
        return token

    async def get_user(self, user_id: str) -> User:
        """
        Obtener usuario por id. Lanza NotFoundError si no existe.
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user
