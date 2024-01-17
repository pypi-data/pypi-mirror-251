from typing import Optional, Final, Iterable


class ClaimTypes:
    Name = "ClaimTypesName"
    Role = "ClaimTypesRole"


class Claim:
    def __init__(
            self,
            claim_type: str,
            claim_value: str,
            issuer: Optional[str] = None,
            subject: Optional["ClaimsIdentity"] = None

    ) -> None:
        self.claim_type: str = claim_type
        self.claim_value: str = claim_value
        self.issuer: str = issuer or ClaimsIdentity.DEFAULT_ISSUER
        self.subject: Optional[str] = subject

    def clone(self) -> "Claim":
        return Claim(**self.__dict__)


class ClaimsIdentity:
    DEFAULT_ISSUER: Final[str] = "@LOCAL AUTHORITY"
    DEFAULT_NAME_CLAIM_TYPE: Final[str] = ClaimTypes.Name
    DEFAULT_ROLE_CLAIM_TYPE: Final[str] = ClaimTypes.Role

    def __init__(
            self,
            *,
            identity: Optional["ClaimsIdentity"] = None,
            claims: Optional[Iterable[Claim]] = None,
            authentication_type: str = None,
            name_type: Optional[str] = None,
            role_type: Optional[str] = None
    ) -> None:
        self._authentication_type: Optional[str] = (
            identity.authentication_type if identity and not authentication_type else authentication_type
        )
        self._name_claim_type: str = self._nct(name_type, identity)
        self._role_claim_type: str = self._nct(role_type, identity)
        self._claims: list[Claim] = list(claims) if claims else []

    @property
    def authentication_type(self) -> Optional[str]:
        return self._authentication_type

    @property
    def is_authenticated(self) -> bool:
        return bool(self._authentication_type)

    @property
    def name_claim_type(self) -> str:
        return self._name_claim_type

    @property
    def role_claim_type(self) -> str:
        return self._role_claim_type

    def _nct(self, name_type: str, claim_identity: "ClaimsIdentity"):
        return (
            name_type if name_type else (
                claim_identity._name_claim_type if claim_identity else self.DEFAULT_NAME_CLAIM_TYPE
            )
        )

    def _rct(self, role_type: str, claim_identity: "ClaimsIdentity"):
        return (
            role_type if role_type else (
                claim_identity._role_claim_type if claim_identity else self.DEFAULT_ROLE_CLAIM_TYPE
            )
        )

    # username
    @property
    def name(self):
        """"""
        if claim := self.find_first(self._name_claim_type):
            return claim.claim_value
        return None

    @property
    def claims(self):
        """"""
        for claim in self._claims:
            yield claim

    def find_all(self, claim_type: str):
        """

        :param claim_type:
        :return:
        """
        for claim in self._claims:
            if claim.claim_type.casefold() == claim_type.casefold():
                yield claim

    def find_first(self, claim_type: str):
        """

        :param claim_type:
        :return:
        """
        for claim in self._claims:
            if claim.claim_type.casefold() == claim_type.casefold():
                return claim
        return None

    def has_claim(self, claim_type: str, claim_value: str):
        """

        :param claim_type:
        :param claim_value:
        :return:
        """
        for claim in self._claims:
            if (
                    claim.claim_type.casefold() == claim_type.casefold() and
                    claim.claim_value == claim_value
            ):
                return True
        return False

    def add_claim(self, claim: Claim):
        self._claims.append(claim)

    def add_claims(self, *claims: Claim):
        self._claims.extend(claims)

    def remove_claim(self, claim: Claim):
        pass

    def try_remove_claim(self, claim: Claim):
        pass


class ClaimsPrincipal:  # User
    def __init__(
            self,
            identity: Optional[ClaimsIdentity] = None
    ) -> None:
        self._identities: list[ClaimsIdentity] = list()

        if isinstance(identity, ClaimsIdentity):
            self._identities.append(identity)
        else:
            self._identities.append(ClaimsIdentity(identity=identity))

    def add_identity(self, identity: ClaimsIdentity):
        """"""
        self._identities.append(identity)

    def add_identities(self, *identities: ClaimsIdentity):
        """"""
        self._identities.extend(identities)

    @property
    def identities(self) -> list[ClaimsIdentity]:
        return self._identities

    @property
    def claims(self):
        """"""
        for identity in self._identities:
            for claim in identity.claims:
                yield claim

    # def create_claims_identity(self, cookie):
    #     return ClaimsIdentity(cookie)

    def find_all(self, claim_type: str):
        """

        :param claim_type:
        :return:
        """
        for identity in self._identities:
            for claim in identity.find_all(claim_type):
                yield claim

    def find_first(self, claim_type: str) -> Optional[Claim]:
        """

        :param claim_type:
        :return:
        """
        for identity in self._identities:
            if claim := identity.find_first(claim_type):
                return claim
        return None

    def has_claim(self, claim_type: str, value: str) -> bool:
        """

        :param claim_type:
        :param value:
        :return:
        """
        for identity in self._identities:
            if identity.has_claim(claim_type, value):
                return True
        return False

    def is_in_role(self, role: str) -> bool:
        """

        :param role:
        :return:
        """
        for identity in self._identities:
            if identity.has_claim(identity.role_claim_type, role):
                return True
        return False

    def find_first_value(self, claim_type: str):
        if claim := self.find_first(claim_type):
            return claim.claim_value
