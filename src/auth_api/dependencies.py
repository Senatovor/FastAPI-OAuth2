from fastapi import Depends
from typing import Annotated
from loguru import logger
from jose import JWTError

from src.database.session import SessionDepends
from .service import UserService
from .utils import oauth2_scheme, decode_jwt
from .exceptions import NotAuthException


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: SessionDepends()
):
    """Получает текущего пользователя по JWT токену.

    Args:
        token: JWT токен
        session: Сессия базы данных

    Returns:
        Объект пользователя

    Raises:
        NotAuthException: Если токен невалидный или пользователь не найден
    """
    try:
        payload = decode_jwt(token)
        username = payload.get('sub')
        if username is None:
            raise NotAuthException
    except JWTError as e:
        logger.error(f'Во время декодирования произошла ошибка: {e}')
        raise NotAuthException
    user = await UserService.find_by_username(session, username)
    if user is None:
        logger.error('Не найден пользователь')
        raise NotAuthException

    return user


