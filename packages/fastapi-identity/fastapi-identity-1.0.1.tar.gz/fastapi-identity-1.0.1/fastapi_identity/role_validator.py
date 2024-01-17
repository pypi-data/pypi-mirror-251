from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, Optional

from pydentity.error_describer import IdentityErrorDescriber
from pydentity.exc import ArgumentNoneError
from pydentity.identity_result import IdentityResult
from pydentity.types import TRole
from pydentity.utils import isnull

if TYPE_CHECKING:
    from pydentity.role_manager import RoleManager


class IRoleValidator(Generic[TRole], ABC):
    """Provides an abstraction for a validating a role."""

    @abstractmethod
    async def validate(self, manager: 'RoleManager[TRole]', role: TRole) -> IdentityResult:
        """
        Validates a role as an asynchronous operation.

        :param manager: The RoleManager[TRole] that can be used to retrieve role properties.
        :param role: The roel to validate.
        :return:
        """


class RoleValidator(IRoleValidator[TRole], Generic[TRole]):
    """Provides the default validation of roles."""

    def __init__(self, errors: Optional[IdentityErrorDescriber] = None):
        """

        :param errors: The IdentityErrorDescriber used to provider error messages.
        """
        self._describer = errors or IdentityErrorDescriber

    async def validate(self, manager: 'RoleManager[TRole]', role: TRole) -> IdentityResult:
        if manager is None:
            raise ArgumentNoneError("manager")
        if role is None:
            raise ArgumentNoneError("role")

        errors = []

        await self._validate_role_name(manager, role, errors)

        if not errors:
            return IdentityResult.success()

        return IdentityResult.failed(*errors)

    async def _validate_role_name(self, manager: 'RoleManager[TRole]', role: TRole, errors):
        role_name = await manager.get_role_name(role)
        if not isnull(role_name):
            if owner := await manager.find_by_name(role_name):
                if await manager.get_role_id(owner) != await manager.get_role_id(role):
                    errors.append(self._describer.DuplicateRoleName(role_name))
        else:
            errors.append(self._describer.InvalidRoleName(role_name))
