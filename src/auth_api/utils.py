from fastapi.security import OAuth2PasswordBearer
from pydantic import SecretStr
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from src.config import config


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth_api/token")


def get_password_hash(password: SecretStr) -> str:
    """Генерирует хеш пароля.

    Args:
        password: Пароль в чистом виде

    Returns:
        Хешированная строка пароля
    """
    return pwd_context.hash(password.get_secret_value())


def verify_password(
        plain_password: str,
        hashed_password: str
) -> bool:
    """Проверяет соответствие пароля и его хеша.

    Args:
        plain_password: Пароль в чистом виде
        hashed_password: Хешированный пароль

    Returns:
        bool: True если пароль верный, иначе False
    """
    return pwd_context.verify(plain_password, hashed_password)


def encode_jwt(
        payload: dict,
        secret_key: str = config.SECRET_KEY,
        algorithm: str = config.ALGORITHM
) -> str:
    """Кодирует данные в JWT токен.

    Args:
        payload: Данные для кодирования
        secret_key: Ключ для подписи (по умолчанию из config)
        algorithm: Алгоритм шифрования (по умолчанию из config)

    Returns:
        Закодированный JWT токен
    """
    encoded = jwt.encode(
        payload,
        secret_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
        token: str | bytes,
        secret_key: str = config.SECRET_KEY,
        algorithm: str = config.ALGORITHM
) -> dict:
    """Декодирует JWT токен.

    Args:
        token: Токен для декодирования
        secret_key: Ключ для проверки подписи (по умолчанию из config)
        algorithm: Алгоритм шифрования (по умолчанию из config)

    Returns:
        Раскодированные данные из токена

    Raises:
        JWTError: Если токен невалидный
    """
    decoded = jwt.decode(
        token,
        secret_key,
        algorithms=[algorithm],
    )
    return decoded


def create_token(
        data: dict,
        type_token: str,
        timedelta_minutes: int
) -> str:
    """Создает JWT токен с указанными параметрами.

    Args:
        data: Основные данные токена
        type_token: Тип токена (например 'accessToken')
        timedelta_minutes: Время жизни токена в минутах

    Returns:
        Сгенерированный JWT токен
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=timedelta_minutes)
    encode = data.copy()
    encode.update({"exp": expire, 'type': type_token})
    token = jwt.encode(
        encode,
        key=config.SECRET_KEY,
        algorithm=config.ALGORITHM
    )
    return token
