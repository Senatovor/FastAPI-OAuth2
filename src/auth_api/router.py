from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from typing import Annotated

from ..database.session import DbSessionDepends
from .service import AuthService
from .schemes import RegistrateUserScheme
from .schemes import TokenScheme

auth_api_router = APIRouter(
    prefix='/auth_api',
    tags=['auth'],
)


@auth_api_router.post('/token', name='token', response_model=TokenScheme)
async def token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db_session: DbSessionDepends(),
) -> TokenScheme:
    return await AuthService.get_token(form_data, db_session)


@auth_api_router.post('/register', name='register', response_class=JSONResponse)
async def register(
        register_user: RegistrateUserScheme,
        session: DbSessionDepends(commit=True)
):
    return await AuthService.register(register_user, session)
