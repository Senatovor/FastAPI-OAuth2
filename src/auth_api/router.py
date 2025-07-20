from fastapi import APIRouter, Form, Response, Depends, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from loguru import logger

from ..config import config
from ..utils import error_response_docs, ok_response_docs
from ..exceptions import ServerException
from ..database.session import SessionDepends
from .service import UserService
from .schemes import RegistrateUser
from .utils import get_password_hash, create_token
from .schemes import Token
from .exceptions import NotAuthException, AlreadyExistException

auth_api_router = APIRouter(
    prefix='/auth_api',
    tags=['auth'],
)


@auth_api_router.post(
    '/token',
    name='token',
    response_model=Token,
    summary="Получение JWT токена",
    description=
    """
    Аутентификация по логину и паролю с получением JWT токена.

    Токен необходимо передавать в заголовке Authorization: Bearer <token>
    """,
    responses={
        **ok_response_docs(
            'Успешная аутентификация'
        ),
        **error_response_docs(
            NotAuthException,
            "Неверные учетные данные или пользователь не найден"
        )
    }
)
async def login_with_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: SessionDepends(),
) -> Token:
    """Аутентификация пользователя и получение JWT токена.

    Args:
        form_data: Данные формы с username и password
        session: Сессия базы данных

    Returns:
        Объект Token с access токеном

    Raises:
        NotAuthException(401): HTTP 401 если аутентификация не удалась
    """
    user = await UserService.get_authenticate_user(
        session,
        form_data.username,
        form_data.password
    )
    if not user:
        logger.warning('Не удачный вход в систему')
        raise NotAuthException

    access_token = create_token(
        data={
            "sub": user.username,
        },
        type_token='accessToken',
        timedelta_minutes=config.ACCESS_TOKEN_EXPIRE
    )

    logger.info(f'Пользователь {user.username} вошел в систему')
    return Token(
        access_token=access_token,
        token_type='Bearer'
    )


@auth_api_router.post(
    '/register',
    name='register',
    response_class=JSONResponse,
    summary="Регистрация пользователя",
    description=
    """
    Создание нового пользователя в системе.
    
    Требует уникального username и password.
    """,
    responses={
        **ok_response_docs(
            'Успешная регистрация'
        ),
        **error_response_docs(
            AlreadyExistException,
            'Пользователь уже существует'
        ),
        **error_response_docs(
            ServerException,
            "Ошибка сервера"
        )
    }
)
async def register(
        register_user: RegistrateUser,
        session: SessionDepends(commit=True)
):
    """Регистрация нового пользователя.

    Args:
        register_user: Данные для регистрации (username, password)
        session: Сессия базы данных с auto-commit

    Returns:
        JSONResponse с сообщением об успешной регистрации

    Raises:
        AlreadyExistException(409): Если пользователь уже существует
        ServerException(500): При других ошибках базы данных
    """
    try:
        register_user.password = get_password_hash(register_user.password)
        user = await UserService.add(session, register_user)
        logger.info(f'Пользователь {user.username} зарегистрирован')
        return JSONResponse(
            content={"message": 'Вы авторизированны'},
            status_code=status.HTTP_200_OK
        )

    except IntegrityError as e:
        if "unique constraint" in str(e.orig).lower():
            logger.error('Такой пользователь уже есть')
            raise AlreadyExistException
        logger.error(f'Ошибка - IntegrityError: {e}')
        raise ServerException
