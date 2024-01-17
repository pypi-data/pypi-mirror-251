import logging
from typing import Generic, Optional

from fastapi_identity.confirmation import IUserConfirmation, DefaultUserConfirmation
from fastapi_identity.core.exc import ArgumentNoneError, InvalidOperationException
from fastapi_identity.core.http_context import HttpContext
from fastapi_identity.options import IdentityOptions
from fastapi_identity.core.claims import ClaimsPrincipal, IdentityConstants
from fastapi_identity.signin_result import SignInResult
from fastapi_identity.types import TUser, HttpContextDependencyCallable
from fastapi_identity.user_claims_principal_factory import IUserClaimsPrincipalFactory
from fastapi_identity.user_manager import UserManager


class SignInManager(Generic[TUser]):
    """Provides the APIs for user sign in."""

    def __init__(
            self,
            context: HttpContext,
            user_manager: UserManager[TUser],
            *,
            claims_factory: IUserClaimsPrincipalFactory[TUser],
            confirmation: IUserConfirmation[TUser],
            options: Optional[IdentityOptions] = None,
            logger: Optional[logging.Logger] = None
    ):
        if user_manager is None:
            raise ArgumentNoneError("user_manager")
        if claims_factory is None:
            raise ArgumentNoneError("claims_factory")

        self._context = context
        self.user_manager: UserManager[TUser] = user_manager
        self.options: IdentityOptions = options or IdentityOptions()
        self.claims_factory: IUserClaimsPrincipalFactory[TUser] = claims_factory
        self._confirmation = confirmation or DefaultUserConfirmation()
        self.logger: logging.Logger = logger or logging.Logger(self.__class__.__name__)
        self.authentication_scheme = IdentityConstants.ApplicationScheme

    @property
    def context(self):
        if self._context is None:
            raise InvalidOperationException("HttpContext must not be None.")
        return self._context

    @context.setter
    def context(self, value):
        self._context = value

    async def create_user_principal(self, user: TUser) -> ClaimsPrincipal:
        """

        :param user:
        :return:
        """
        return await self.claims_factory.create(user)

    async def is_signed_in(self, principal: ClaimsPrincipal):
        """

        :param principal:
        :return:
        """
        if principal is None:
            raise ArgumentNoneError("principal")
        return principal.identities and any(
            i for i in principal.identities if i.authentication_type == self.authentication_scheme
        )

    async def signin_with_claims(self, user: TUser, claims):
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
            self.logger.debug("User cannot sign in without a confirmed email.")
            return False

        if (
                self.options.SignIn.REQUIRED_CONFIRMED_PHONE_NUMBER and
                not await self.user_manager.is_phone_number_confirmed(user)
        ):
            self.logger.debug("User cannot sign in without a confirmed phone number.")
            return False

        if (
                self.options.SignIn.REQUIRE_CONFIRMED_ACCOUNT and
                not await self._confirmation.is_confirmed(self.user_manager, user)
        ):
            self.logger.debug("User cannot sign in without a confirmed account.")
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
        return security_stamp and user is not None and security_stamp == user.security_stamp

    async def password_sign_in(
            self,
            username: str,
            password: str,
            is_persistent: bool = False,
            lockout_on_failure: bool = True
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

        return await self.check_password_sign_in(user, password, is_persistent, lockout_on_failure), user

    async def check_password_sign_in(
            self,
            user: TUser,
            password: str,
            is_persistent: bool,
            lockout_on_failure: bool
    ) -> SignInResult:
        """

        :param user:
        :param password:
        :param is_persistent:
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
                raise InvalidOperationException("ResetLockout failed.")

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


SignInManagerDependency = HttpContextDependencyCallable[SignInManager[TUser]]
