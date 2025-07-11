from fastapi import status
from fastapi.exceptions import HTTPException

NotAuthException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Вы не авторизированны",
    headers={"WWW-Authenticate": "Bearer"}
)
"""Исключение для ошибок аутентификации.

Возникает когда:
- Не предоставлены учетные данные
- Неверные учетные данные
- Истек срок действия токен
"""

AlreadyExistException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Конфликт: данные уже существуют",
)
"""Исключение для конфликтов данных.

Возникает когда:
- Пользователь с таким username уже существует
- Попытка создать дублирующую запись
"""