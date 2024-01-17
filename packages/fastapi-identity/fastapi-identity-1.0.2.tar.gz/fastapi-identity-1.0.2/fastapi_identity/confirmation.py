from abc import ABC, abstractmethod
from typing import Generic

from fastapi_identity import UserManager
from fastapi_identity.types import TUser


class IUserConfirmation(Generic[TUser], ABC):
    @abstractmethod
    async def is_confirmed(self, manager: UserManager, user: TUser) -> bool:
        """

        :param manager:
        :param user:
        :return:
        """


class DefaultUserConfirmation(IUserConfirmation[TUser], Generic[TUser]):
    async def is_confirmed(self, manager: UserManager, user: TUser) -> bool:
        return await manager.is_email_confirmed(user)
