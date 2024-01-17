from typing import Type, Annotated, Callable

from fastapi import APIRouter, Depends, status, HTTPException

from pydentity.role_manager import RoleManager
from pydentity.schemas import BaseCreateRole, BaseRole


def get_create_role_router(
        factory_role_manager: Callable[..., RoleManager],
        role_schema: Type[BaseRole] = BaseRole,
        create_role_schema: Type[BaseCreateRole] = BaseCreateRole,
        path="/create-role"
):
    router = APIRouter()

    @router.post(
        path,
        response_model=role_schema,
        status_code=status.HTTP_201_CREATED,
    )
    async def create_role(
            form: Annotated[create_role_schema, Depends()],
            role_manager: Annotated[RoleManager, Depends(factory_role_manager)]
    ):
        role = role_manager.create_model_from_schema(form)
        result = await role_manager.create(role)
        if not result.succeeded:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=[err.description for err in result.errors]
            )
        return role_schema.model_validate(role)

    return router
