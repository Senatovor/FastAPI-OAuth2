from pydantic import BaseModel, EmailStr, Field, SecretStr


class SystemUserScheme(BaseModel):
    """Форма юзера"""
    username: str = Field(..., description='Имя пользователя')
    email: EmailStr = Field(..., description='Почта пользователя')


class RegistrateUser(SystemUserScheme):
    """Форма регистрации пользователя"""
    password: SecretStr = Field(..., description='Введенный пароль, в дальнейшем хэшируется')


class Token(BaseModel):
    """Модель токена аунтефикации"""
    access_token: str = Field(..., description='Токен')
    token_type: str = Field(..., description='Тип токена')
