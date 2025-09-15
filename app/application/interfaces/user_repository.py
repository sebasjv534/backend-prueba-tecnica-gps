from app.domain.models.user_model import User

class IUserRepository:
    async def get_by_username(self, username: str) -> User | None:
        raise NotImplementedError

    async def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    async def get_by_id(self, user_id: str) -> User | None:
        raise NotImplementedError

    async def create(self, user: User) -> User:
        raise NotImplementedError
