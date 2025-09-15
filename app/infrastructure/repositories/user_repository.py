from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.domain.models.user_model import User
from app.application.interfaces.user_repository import IUserRepository

class UserRepositorySQLAlchemy(IUserRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_username(self, username: str) ->  User | None:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalars().first()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_by_id(self, user_id: str) -> User | None:
        try:
            # Convertir string a UUID
            uuid_id = UUID(user_id)
            result = await self.db.execute(select(User).where(User.id == uuid_id))
            return result.scalars().first()
        except ValueError:
            # Si el string no es un UUID válido, retornar None
            return None

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
