from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from ..database.service import BaseService
from .models import User
from .utils import verify_password


class UserService(BaseService):
    model = User

    @classmethod
    async def find_by_username(cls, session: AsyncSession, username: str) -> model:
        """Нахождение юзера по username.

        Args:
            session: Aссинхронная сессия базы данных
            username: Логин пользователя

        Returns:
            Объект пользователя
        """
        try:
            query = select(cls.model).filter_by(username=username)
            result = await session.execute(query)
            find_object = result.scalar_one_or_none()
            return find_object
        except SQLAlchemyError as e:
            raise e

    @classmethod
    async def get_authenticate_user(
            cls,
            session: AsyncSession,
            username: str,
            password: str
    ):
        """Получает и аутентифицирует пользователя по логину и паролю.

        Args:
            session: Aссинхронная сессия базы данных
            username: Логин пользователя
            password: Пароль в чистом виде

        Returns:
            Объект пользователя если аутентификация успешна, иначе False
        """
        user = await cls.find_by_username(session, username)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user