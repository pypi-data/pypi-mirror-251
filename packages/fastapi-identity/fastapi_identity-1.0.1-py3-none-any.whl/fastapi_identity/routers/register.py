from typing import Type, Annotated

from fastapi import APIRouter, HTTPException, Depends, status

from pydentity.schemas import BaseUser, BaseRegisterUser
from pydentity.types import TUser
from pydentity.user_manager import UserManager, UserManagerDependency


def get_register_router(
        factory_user_manager: UserManagerDependency[TUser],
        user_schema: Type[BaseUser] = None,
        user_register_schema: Type[BaseRegisterUser] = None
):
    router = APIRouter()

    if user_schema is None:
        user_schema = BaseUser
    if user_register_schema is None:
        user_register_schema = BaseRegisterUser

    @router.post("/register", status_code=status.HTTP_201_CREATED)
    async def register(
            user_manager: Annotated[UserManager[TUser], Depends(factory_user_manager)],
            form: user_register_schema
    ):
        user = user_manager.create_model_from_schema(form)
        result = await user_manager.create(user, form.password)
        if not result.succeeded:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=[err.description for err in result.errors]
            )
        return user_schema.model_validate(user)

    return router
