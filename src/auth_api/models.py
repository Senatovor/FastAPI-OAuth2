from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text

from src.database.model import Base


class User(Base):
    """ORM-модель пользователя системы.

    Attributes:
        username: Логин пользователя. Обязательное поле.
        email: Электронная почта пользователя. Должна быть уникальной.
        password: Хэшированный пароль пользователя. Хранится в зашифрованном виде.
        role: Роль пользователя в системе. По умолчанию 'user'.
    """
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)

    role: Mapped[str] = mapped_column(
        default='user',
        server_default=text('user'),
        nullable=False,
    )
