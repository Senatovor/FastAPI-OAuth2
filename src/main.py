from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel

from src.database.session import session_manager
from src.log import setup_logger
from src.config import config
from src.auth_api.router import auth_api_router
from src.users.router import users_router


class AppState(BaseModel):
    redis_manager: Any
    db_manager: Any


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Контекстный менеджер для управления жизненным циклом приложения.

    Args:
        app: Экземпляр FastAPI приложения
    """
    app.state: AppState

    # Инициализация сессий sql базы
    await session_manager.init()

    app.state.db_manager = session_manager

    yield

    # Очистка
    await app.state.redis_manager.close()
    await app.state.db_manager.close()


def create_app() -> FastAPI:
    """Фабрика для создания и настройки экземпляра FastAPI.

    Returns:
        FastAPI: Настроенный экземпляр FastAPI приложения
    """
    app = FastAPI(
        title=config.TITLE,
        version=config.VERSION,
        description=config.description_project,
        contact=config.contact_project,
        docs_url=config.DOCS_URL,
        redoc_url=config.REDOC_URL,
        lifespan=lifespan
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(auth_api_router)  # Установка роутера авторизации
    app.include_router(users_router)

    return app


if __name__ == '__main__':
    try:
        setup_logger()
        app = create_app()
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=5000,
            log_config=None,
            log_level=None,
        )

    except Exception as e:
        logger.error(f'Во время создания приложения произошла ошибка: {e}')
