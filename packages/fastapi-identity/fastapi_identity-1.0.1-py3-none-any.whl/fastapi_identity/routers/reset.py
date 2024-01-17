from typing import Callable, Awaitable, Annotated, Coroutine

from fastapi import APIRouter, Depends, Query, HTTPException, Body
from pydantic import EmailStr
from starlette import status

from pydentity.schemas import BaseResetPassword
from pydentity.types import TUser
from pydentity.user_manager import UserManager, UserManagerDependency


def get_reset_password_router(
        get_user_manager: UserManagerDependency[TUser],
        after_forgot_password: Callable[[UserManager, TUser, str], Coroutine],
        override_forgot_path: str = None,
        override_reset_path: str = None
) -> APIRouter:
    """

    :param override_reset_path: Default '/forgot-password'
    :param override_forgot_path: Default '/reset-password'
    :param get_user_manager:
    :param after_forgot_password: (user_manager, user, token) -> ...
    :return:

    Details:

    app = FastAPI()
    app.include_router(get_reset_password_router(factory, my_forgot_callback), prefix='/oauth')

    async def my_forgot_callback(manager, user, token):
        url = f'https://127.0.0.1/reset-password?token={token}'
        email_service.send(_from='SecuritySite', _to=user.email, message=f'Click the link {url}')
    """
    if override_forgot_path is None:
        override_forgot_path = '/forgot-password'

    if override_reset_path is None:
        override_reset_path = '/reset-password'

    router = APIRouter()

    @router.post(
        override_forgot_path,
        status_code=status.HTTP_200_OK,
    )
    async def forgot_password(
            user_manager: Annotated[UserManager[TUser], Depends(get_user_manager)],
            email: EmailStr = Body(embed=True)
    ):
        if user := await user_manager.find_by_email(email):
            token = await user_manager.generate_password_reset_token(user)
            await after_forgot_password(user_manager, user, token)

    @router.post(
        override_reset_path,
        status_code=status.HTTP_200_OK,
    )
    async def reset_password(
            user_manager: Annotated[UserManager[TUser], Depends(get_user_manager)],
            token: Annotated[str, Query()],
            form: BaseResetPassword,
    ):
        user = await user_manager.find_by_email(form.email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=["Invalid token."]
            )

        result = await user_manager.reset_password(user, token, form.password)
        if not result.succeeded:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=[err.description for err in result.errors]
            )

    return router
