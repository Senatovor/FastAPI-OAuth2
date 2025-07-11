from pydantic import BaseModel, EmailStr, Field, SecretStr


class RegistrateUser(BaseModel):
    """Форма регистрации пользователя"""
    username: str = Field(..., description='Имя пользователя')
    email: EmailStr = Field(..., description='Почта пользователя')
    password: SecretStr = Field(..., description='Введенный пароль, в дальнейшем хэшируется')


class Token(BaseModel):
    """Модель токена аунтефикации"""
    access_token: str = Field(..., description='Токен')
    token_type: str = Field(..., description='Тип токена')
