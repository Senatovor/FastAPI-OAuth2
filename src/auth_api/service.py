from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from .models import User
from .handler import AuthHandler
from .schemes import Token, RegistrateUser
from ..config import config
from ..database.executer import sql_manager


class AuthService:
    @staticmethod
    async def get_token(form_data: OAuth2PasswordRequestForm, db_session: AsyncSession):
        try:
            user = await sql_manager(
                select(User).where(User.username == form_data.username)
            ).scalar_one_or_none(db_session)
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не верные username или пароль')
            if not AuthHandler.verify_password(form_data.password, user.password):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не верные username или пароль')
            access_token = await AuthHandler.create_token(
                data={
                    "sub": user.username,
                },
                token_type='accessToken',
                timedelta_minutes=config.auth_config.ACCESS_TOKEN_EXPIRE
            )
            return Token(
                access_token=access_token,
                token_type='Bearer'
            )
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Ошибка сервера')

    @staticmethod
    async def register(register_user: RegistrateUser, db_session: AsyncSession):
        try:
            register_user.password = await AuthHandler.get_password_hash(register_user.password)
            user = await sql_manager(
                insert(User).values(**register_user.model_dump()).returning(User)
            ).scalar_one_or_none(db_session)
            logger.info(f'Пользователь {user.username} зарегистрирован')
            return JSONResponse(
                content={"message": 'Вы авторизированны'},
                status_code=status.HTTP_200_OK
            )

        except IntegrityError as e:
            if "unique constraint" in str(e.orig).lower():
                logger.error('Такой пользователь уже есть')
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Конфликт: данные уже существуют")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка сервера")
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Ошибка сервера')
