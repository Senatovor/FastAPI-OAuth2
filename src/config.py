from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr, HttpUrl
from pathlib import Path
from loguru import logger


class Config(BaseSettings):
    """
    Основной класс конфигурации приложения.

    Загружает настройки из .env файла или переменных окружения.
    Все чувствительные данные должны быть указаны в .env файле.

    Attributes:
        DB_HOST (str): Хост базы данных
        DB_PORT (str): Порт базы данных
        POSTGRES_DB (str): Имя базы данных
        POSTGRES_USER (str): Пользователь БД
        POSTGRES_PASSWORD (str): Пароль пользователя БД
        SECRET_KEY (str): Секретный ключ для JWT
        ALGORITHM (str): Алгоритм шифрования JWT
        ACCESS_TOKEN_EXPIRE (int): Время жизни access токена (в минутах)
        TITLE (str): Имя проекта
        VERSION (str): Версия проекта
        DESCRIPTION (str): Описание проекта (можно использовать синтаксис .md файлов):
        NAME_AUTHOR (str or None): Автор проекта
        URL_AUTHOR (str or None): Ссылка на автора проекта
        EMAIL_AUTHOR (str or None): Почта автора проекта
        DOCS_URL (str or None): http путь к документации docs
        REDOC_URL (str or None): http путь к документации redocs
        ROOT_PATH (str or None): http корневой путь проекта
        ROTATION (str or None): При каком условии происходит ротация логов
        LEVEL (str or None): Уровень логирования
        COMPRESSION (str or None): Формат сжатия логов
        BACKTRACE (bool): Включает подробный трейсбек при ошибках
        DIAGNOSE (bool): Добавляет информацию о переменных в стектрейс
        ENQUEUE (bool): Асинхронная запись логов
        CATCH (bool): Перехватывание исключения
    """
    # Настройки базы данных
    DB_HOST: str
    DB_PORT: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # Настройки аутентификации
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE: int

    # Настройка приложения
    TITLE: str = 'FastAPI'
    VERSION: str = '1.0.0'
    DESCRIPTION: str | None = None
    NAME_AUTHOR: str | None = None
    URL_AUTHOR: HttpUrl | None = None
    EMAIL_AUTHOR: EmailStr | None = None
    DOCS_URL: str | None = None
    REDOC_URL: str | None = None
    ROOT_PATH: str | None = None
    ROTATION: str | None = None
    LEVEL: str | None = None
    COMPRESSION: str | None = None
    BACKTRACE: bool
    DIAGNOSE: bool
    ENQUEUE: bool
    CATCH: bool

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        env_file_encoding='utf-8'
    )

    def get_db_url(self) -> str:
        """
        Генерирует URL для подключения к PostgreSQL с использованием asyncpg.

        1. Формирует строку подключения из параметров
        2. Логирует факт генерации (без пароля)
        3. Возвращает готовый URL

        Returns:
            str: Строка подключения к базе данных
        """
        return (f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
                f'{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}')

    def get_description(self) -> str:
        """Возвращает описание проекта"""
        return self.DESCRIPTION or None

    def get_contact(self) -> dict:
        """Возвращает контактные данные автора проекта"""
        return {
            "name": self.NAME_AUTHOR or None,
            "url": self.URL_AUTHOR or None,
            "email": self.EMAIL_AUTHOR or None,
        }


try:
    config = Config()
except Exception as e:
    logger.error(f'Во время парсинга .env произошла ошибка: {e}')
