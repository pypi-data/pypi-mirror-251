import logging
from typing import Generic, Optional, Iterable

from pydentity.exc import ArgumentNoneError
from pydentity.options import IdentityOptions
from pydentity.claims import ClaimsPrincipal
from pydentity.signin_result import SignInResult
from pydentity.types import TUser
from pydentity.user_claims_principal_factory import IUserClaimsPrincipalFactory
from pydentity.user_manager import UserManager


class IdentityResultError(Exception):
    def __init__(self):
        super().__init__("IdentityError", "ResetLockout failed.")


class SignInManager(Generic[TUser]):
    """Provides the APIs for user sign in."""

    def __init__(
            self,
            user_manager: UserManager[TUser],
            *,
            options: Optional[IdentityOptions] = None,
            user_claims_principal_factory: IUserClaimsPrincipalFactory[TUser] = None,
            logger: Optional[logging.Logger] = None
    ):
        """

        :param user_manager:
        :param options:
        :param logger:
        """
        self.user_manager: UserManager[TUser] = user_manager
        self.options = options or self.user_manager.options
        self.user_claims_principal_factory: IUserClaimsPrincipalFactory[TUser] = user_claims_principal_factory
        self.logger: logging.Logger = logger or logging.Logger(self.__class__.__name__)

    async def is_signed_in(self, principal: ClaimsPrincipal):
        pass

    async def refresh_sign_in(self, user: TUser):
        pass

    async def can_sign_in(self, user: TUser) -> bool:
        """
        Returns a flag indicating whether the specified user can sign in.

        :param user: The user whose sign-in status should be returned.
        :return:
        """
        if (
                self.options.SignIn.REQUIRE_CONFIRMED_EMAIL and
                not await self.user_manager.is_email_confirmed(user)
        ):
            self.logger.warning("User cannot sign in without a confirmed email.")
            return False

        if (
                self.options.SignIn.REQUIRED_CONFIRMED_PHONE_NUMBER and
                not await self.user_manager.is_phone_number_confirmed(user)
        ):
            self.logger.warning("User cannot sign in without a confirmed phone number.")
            return False

        return True

    async def validate_security_stamp(self, user: TUser, security_stamp: str) -> bool:
        """
        Validates the security stamp for the specified user.
        If no user is specified, or if the stores does not support security stamps, validation is considered successful.

        :param user: The user whose stamp should be validated.
        :param security_stamp: The expected security stamp value.
        :return: The result of the validation.
        """
        return security_stamp and user is not None and (security_stamp == user.security_stamp)

    async def password_sign_in(
            self,
            username: str,
            password: str,
            is_persistent: bool,
            lockout_on_failure: bool
    ) -> tuple[SignInResult, TUser]:
        """

        :param username:
        :param password:
        :param is_persistent:
        :param lockout_on_failure:
        :return:
        """
        user = await self.user_manager.find_by_name(username)

        if not user:
            return SignInResult.failed(), user

        return await self.check_password_sign_in(user, password, lockout_on_failure), user

    async def check_password_sign_in(self, user: TUser, password: str, lockout_on_failure: bool) -> SignInResult:
        """

        :param user:
        :param password:
        :param lockout_on_failure:
        :return:
        """
        if not user:
            raise ArgumentNoneError("user")

        if error := await self._pre_sign_in_check(user):
            return error

        if await self.user_manager.check_password(user, password):
            await self.reset_lockout(user)
            return SignInResult.success()

        self.logger.warning("User failed to provide the correct password.")

        if self.user_manager.supports_user_lockout and lockout_on_failure:
            increment_lockout_result = await self.user_manager.access_failed(user)
            if not increment_lockout_result.succeeded:
                return SignInResult.failed()

            if await self.user_manager.is_locked_out(user):
                return await self.locked_out(user)

        return SignInResult.failed()

    async def is_locked_out(self, user: TUser) -> bool:
        """
        Used to determine if a user is considered locked out.

        :param user: The user.
        :return:
        """
        return self.user_manager.supports_user_lockout and await self.user_manager.is_locked_out(user)

    async def reset_lockout(self, user: TUser):
        """
        Used to reset a user's lockout count.

        :param user: The user.
        :return:
        """
        if self.user_manager.supports_user_lockout:
            result = await self.user_manager.reset_access_failed_count(user)

            if not result.succeeded:
                raise IdentityResultError()

    async def locked_out(self, user: TUser) -> SignInResult:
        """
        Returns a locked out SignInResult.

        :param user:
        :return:
        """
        self.logger.warning("User is currently locked out.")
        return SignInResult.locked_out()

    async def _pre_sign_in_check(self, user: TUser) -> Optional[SignInResult]:
        """
        Used to ensure that a user is allowed to sign in.

        :param user:
        :return:
        """
        if not await self.can_sign_in(user):
            return SignInResult.failed()

        if await self.is_locked_out(user):
            return await self.locked_out(user)

        return None

    async def signin_or_two_factor(self, user: TUser, is_persistent: bool):
        pass

    async def signin_with_claims(self, user: TUser, is_persistent: bool, claims: Iterable[Claim]):
        pass

    async def signin_with_claims(
            self,
            user: TUser,
            auth_properties: Optional[AuthenticationProperties],
            claims: Iterable[Claim]
    ):
        user_principal = self.create_user_principal(user)
        for claim in claims:
            pass

    async def create_user_principal(self, user: TUser):
        return self.claims_factory.create(user)
