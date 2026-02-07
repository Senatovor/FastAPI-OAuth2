from fastapi import APIRouter, Depends, Security
from typing import Annotated

from ..auth_api.dependencies import get_current_user
from ..auth_api.schemes import SystemUserScheme

users_router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@users_router.get('/info', name='users-info', response_model=SystemUserScheme)
async def user_info(
        user: Annotated[SystemUserScheme, Security(get_current_user, scopes=['user:all'])]
):
    """Получить основную информацию об авторизированном юзере"""
    return user