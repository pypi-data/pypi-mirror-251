from abc import ABC, abstractmethod
from typing import Generic

from pydentity.exc import ArgumentNoneError
from pydentity.claims import ClaimsPrincipal, ClaimsIdentity, Claim
from pydentity.types import TUser
from pydentity.user_manager import UserManager


class IUserClaimsPrincipalFactory(Generic[TUser], ABC):
    """Provides an abstraction for a factory to create a ClaimsPrincipal from a user."""

    @abstractmethod
    async def create(self, user: TUser) -> ClaimsPrincipal:
        """
        Creates a ClaimsPrincipal from an user.

        :param user: The user to create a ClaimsPrincipal from.
        :return:
        """

    @abstractmethod
    async def generate_claims(self, user: TUser) -> ClaimsIdentity:
        """

        :param user:
        :return:
        """


class UserClaimsPrincipalFactory(IUserClaimsPrincipalFactory[TUser], Generic[TUser]):
    def __init__(self, user_manager: UserManager[TUser]):
        self.user_manager: UserManager[TUser] = user_manager
        self.options = self.user_manager.options

    async def create(self, user: TUser) -> ClaimsPrincipal:
        if not user:
            raise ArgumentNoneError("user")

        identity = await self.generate_claims(user)
        return ClaimsPrincipal(identity=identity)

    async def generate_claims(self, user: TUser) -> ClaimsIdentity:
        user_id = await self.user_manager.get_user_id(user=user)
        username = await self.user_manager.get_username(user=user)
        identity = ClaimsIdentity(
            authentication_type="Pydentity.Application",
            name_type=self.options.ClaimsIdentity.USER_NAME_CLAIM_TYPE,
            role_type=self.options.ClaimsIdentity.ROLE_CLAIM_TYPE,
        )
        identity.add_claim(Claim(self.options.ClaimsIdentity.USER_ID_CLAIM_TYPE, user_id))
        identity.add_claim(Claim(self.options.ClaimsIdentity.USER_NAME_CLAIM_TYPE, username))

        if self.user_manager.supports_user_email:
            if email := await self.user_manager.get_email(user):
                identity.add_claim(Claim(self.options.ClaimsIdentity.EMAIL_CLAIM_TYPE, email))

        if self.user_manager.supports_user_security_stamp:
            if security := await self.user_manager.get_security_stamp(user):
                identity.add_claim(Claim(self.options.ClaimsIdentity.SECURITY_STAMP_CLAIM_TYPE, security))

        if self.user_manager.supports_user_claim:
            if claims := await self.user_manager.get_claims(user):
                identity.add_claims(*claims)

        return identity
