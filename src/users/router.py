from fastapi import APIRouter, Depends
from src.auth_api.dependencies import get_current_user
from src.auth_api.schemes import SystemUser
from typing import Annotated

users_router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@users_router.get(
    '/info',
    name='users-info',
    response_model=SystemUser,
    summary="Получение текущего юзера",
)
async def user_info(user: Annotated[SystemUser, Depends(get_current_user)]):
    return user