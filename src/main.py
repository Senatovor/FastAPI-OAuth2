import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from src.log import setup_logger
from src.config import config
from src.auth_api.router import auth_api_router


def create_app() -> FastAPI:
    """
    Фабрика для создания и настройки экземпляра FastAPI приложения.

    Returns:
        FastAPI: Настроенный экземпляр FastAPI приложения
    """
    app = FastAPI(
        title=config.TITLE,
        version=config.VERSION,
        description=config.get_description(),
        contact=config.get_contact(),
        docs_url=config.DOCS_URL,
        redoc_url=config.REDOC_URL,
        root_path=config.ROOT_PATH,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.include_router(auth_api_router)     # Установка роутера авторизации
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
