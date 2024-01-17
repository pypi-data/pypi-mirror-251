from typing import Optional, Iterable, Generator, Any, Union, overload, Callable

from fastapi_identity.types import Predicate


class IdentityConstants:
    IdentityPrefix: str = "FastAPIIdentity"
    ApplicationScheme: str = IdentityPrefix + ".Application"
    BearerScheme: str = IdentityPrefix + ".Bearer"
    ExternalScheme: str = IdentityPrefix + ".External"
    TwoFactorRememberMeScheme: str = IdentityPrefix + ".TwoFactorRememberMe"
    TwoFactorUserIdScheme: str = IdentityPrefix + ".TwoFactorUserId"


class ClaimTypes:
    AuthenticationInstant = "authenticationinstant"
    AuthenticationMethod = "authenticationmethod"
    CookiePath = "cookiepath"
    DenyOnlyPrimarySid = "denyonlyprimarysid"
    DenyOnlyPrimaryGroupSid = "denyonlyprimarygroupsid"
    DenyOnlyWindowsDeviceGroup = "denyonlywindowsdevicegroup"
    Dsa = "dsa"
    Expiration = "expiration"
    Expired = "expired"
    GroupSid = "groupsid"
    IsPersistent = "ispersistent"
    PrimaryGroupSid = "primarygroupsid"
    PrimarySid = "primarysid"
    Role = "role"
    SerialNumber = "serialnumber"
    UserData = "userdata"
    Version = "version"
    WindowsAccountName = "windowsaccountname"
    WindowsDeviceClaim = "windowsdeviceclaim"
    WindowsDeviceGroup = "windowsdevicegroup"
    WindowsUserClaim = "windowsuserclaim"
    WindowsFqbnVersion = "windowsfqbnversion"
    WindowsSubAuthority = "windowssubauthority"
    Anonymous = "anonymous"
    Authentication = "authentication"
    AuthorizationDecision = "authorizationdecision"
    Country = "country"
    DateOfBirth = "dateofbirth"
    Dns = "dns"
    DenyOnlySid = "denyonlysid"
    Email = "emailaddress"
    Gender = "gender"
    GivenName = "givenname"
    Hash = "hash"
    HomePhone = "homephone"
    Locality = "locality"
    MobilePhone = "mobilephone"
    Name = "name"
    NameIdentifier = "nameidentifier"
    OtherPhone = "otherphone"
    PostalCode = "postalcode"
    Rsa = "rsa"
    Sid = "sid"
    Spn = "spn"
    StateOrProvince = "stateorprovince"
    StreetAddress = "streetaddress"
    Surname = "surname"
    System = "system"
    Thumbprint = "thumbprint"
    Upn = "upn"
    Uri = "uri"
    Webpage = "webpage"
    X500DistinguishedName = "x500distinguishedname"
    Actor = "actor"


class Claim:
    def __init__(
            self,
            _type: str,
            _value: Any,
            issuer: Optional[str] = None,
            original_issuer: Optional[str] = None,
            subject: Optional['ClaimsIdentity'] = None
    ) -> None:
        self._type = _type
        self._value = _value
        self._issuer = issuer
        self._original_issuer = original_issuer
        self._subject = subject

    @property
    def type(self) -> str:
        return self._type

    @property
    def value(self) -> Any:
        return self._value

    @property
    def issuer(self) -> str:
        return self._issuer

    @property
    def original_issuer(self) -> str:
        return self._original_issuer

    @property
    def subject(self) -> Optional['ClaimsIdentity']:
        return self._subject

    def clone(self, identity: 'ClaimsIdentity'):
        return Claim(
            _type=self.type,
            _value=self.value,
            issuer=self.issuer,
            original_issuer=self.original_issuer,
            subject=identity
        )

    def dump(self):
        return {
            '_type': self.type,
            '_value': self.value,
            'issuer': self.issuer or ClaimsIdentity.DefaultIssuer,
            'original_issuer': self.original_issuer or ClaimsIdentity.DefaultIssuer,
            'authentication_type': self.subject.authentication_type
        }

    @staticmethod
    def load(identity: 'ClaimsIdentity', data: dict) -> 'Claim':
        return Claim(
            _type=data.get('_type'),
            _value=data.get('_value'),
            issuer=data.get('issuer'),
            original_issuer=data.get('original_issuer'),
            subject=identity
        )


class ClaimsIdentity:
    DefaultIssuer: str = "@local authority"
    DefaultNameClaimType: str = ClaimTypes.Name
    DefaultRoleClaimType: str = ClaimTypes.Role

    def __init__(
            self,
            authentication_type: Optional[str] = None,
            claims: Optional[Iterable[Claim]] = None
    ) -> None:
        self._authentication_type = authentication_type
        self._instance_claims: list[Claim] = []
        if claims:
            self.add_claims(*claims)

    @property
    def is_authenticated(self) -> bool:
        return bool(self._authentication_type)

    @property
    def authentication_type(self) -> str:
        return self._authentication_type

    @property
    def name(self) -> Optional[str]:
        if claim := self.find_first(ClaimTypes.Name):
            return claim.value
        return None

    @property
    def claims(self) -> Generator[Claim, Any, None]:
        for claim in self._instance_claims:
            yield claim

    def add_name_claim(self, name: str):
        self.add_claims(Claim(ClaimTypes.Name, name))

    def add_role_claim(self, role: str):
        self.add_claims(Claim(ClaimTypes.Role, role))

    def add_claims(self, *claims: Claim):
        """
        Adds claims to internal list. Calling Claim.Clone if Claim.Subject != this.
        """
        for claim in claims:
            if claim.subject is self:
                self._instance_claims.append(claim)
            else:
                self._instance_claims.append(claim.clone(self))

    @overload
    def find_all(self, match: str) -> Generator[Claim, Any, None]:
        ...

    @overload
    def find_all(self, match: Predicate[Claim]) -> Generator[Claim, Any, None]:
        ...

    def find_all(self, match: Union[str, Predicate[Claim]]) -> Generator[Claim, Any, None]:
        _match: Predicate[Claim] = match

        if isinstance(match, str):
            def _match(x): return x.type == match

        for claim in self.claims:
            if _match(claim):
                yield claim

    @overload
    def find_first(self, match: str) -> Optional[Claim]:
        ...

    @overload
    def find_first(self, match: Predicate[Claim]) -> Optional[Claim]:
        ...

    def find_first(self, match: Union[str, Predicate[Claim]]) -> Optional[Claim]:
        _match: Predicate[Claim] = match

        if isinstance(match, str):
            def _match(x): return x.type == match

        for claim in self.claims:
            if _match(claim):
                return claim

    @overload
    def has_claim(self, match: tuple[str, str]) -> bool:
        ...

    @overload
    def has_claim(self, match: Predicate[Claim]) -> bool:
        ...

    def has_claim(self, match: Union[tuple[str, str], Predicate[Claim]]) -> bool:
        _match: Predicate[Claim] = match

        if isinstance(match, tuple):
            type_, value_ = match

            def _match(x: Claim):
                return x.type.casefold() == type_.casefold() and x.value == value_

        for claim in self.claims:
            if _match(claim):
                return True
        return False

    def dump(self):
        _claims = []
        for claim in self.claims:
            _data = claim.dump()
            _data.update({'authentication_type': self.authentication_type})
            _claims.append(_data)
        return _claims

    @staticmethod
    def load(data: dict) -> tuple[str, 'ClaimsIdentity']:
        identity = ClaimsIdentity(authentication_type=data.get('authentication_type'))
        claims = [Claim.load(identity, data)]
        identity.add_claims(*claims)
        return data.get('authentication_type', 'None'), identity


class ClaimsPrincipal:
    def __init__(
            self,
            *identities: ClaimsIdentity
    ) -> None:
        self.primary_identity_selector: Optional[Callable[[Iterable[ClaimsIdentity]], Optional[ClaimsIdentity]]] = None
        self._identities: list[ClaimsIdentity] = list(identities) if identities else []

    @property
    def identities(self) -> list[ClaimsIdentity]:
        return self._identities

    @property
    def claims(self) -> Generator[Claim, Any, None]:
        for identity in self.identities:
            for claim in identity.claims:
                yield claim

    @property
    def identity(self) -> Optional[ClaimsIdentity]:
        if select_primary_identity is not None:
            return select_primary_identity(self._identities)
        else:
            return select_primary_identity(self._identities)

    def add_identities(self, *identities: ClaimsIdentity):
        if not identities:
            raise ValueError
        self._identities.extend(identities)

    @overload
    def find_all(self, match: str) -> Generator[Claim, Any, None]:
        ...

    @overload
    def find_all(self, match: Predicate[Claim]) -> Generator[Claim, Any, None]:
        ...

    def find_all(self, match: Union[str, Predicate[Claim]]) -> Generator[Claim, Any, None]:
        _match: Predicate[Claim] = match

        if isinstance(match, str):
            def _match(x): return x.type == match

        for identity in self.identities:
            for claim in identity.find_all(_match):
                yield claim

    @overload
    def find_first(self, match: str) -> Optional[Claim]:
        ...

    @overload
    def find_first(self, match: Predicate[Claim]) -> Optional[Claim]:
        ...

    def find_first(self, match: Union[str, Predicate[Claim]]) -> Optional[Claim]:
        _match: Predicate[Claim] = match

        if isinstance(match, str):
            def _match(x): return x.type == match

        for identity in self.identities:
            if claim := identity.find_first(_match):
                return claim

    @overload
    def find_first_value(self, match: str) -> Optional[Any]:
        ...

    @overload
    def find_first_value(self, match: Predicate[Claim]) -> Optional[Any]:
        ...

    def find_first_value(self, match: Union[str, Predicate[Claim]]) -> Optional[Any]:
        if _claim := self.find_first(match):
            return _claim.value
        return None

    @overload
    def has_claim(self, match: tuple[str, str]) -> bool:
        ...

    @overload
    def has_claim(self, match: Predicate[Claim]) -> bool:
        ...

    def has_claim(self, match: Union[tuple[str, str], Predicate[Claim]]) -> bool:
        _match: Predicate[Claim] = match

        if isinstance(match, tuple):
            type_, value_ = match

            def _match(x: Claim):
                return x.type.casefold() == type_.casefold() and x.value == value_

        for identity in self.identities:
            if identity.has_claim(_match):
                return True

        return False

    def is_in_role(self, role: str):
        for identity in self.identities:
            if identity.has_claim((ClaimTypes.Role, role)):
                return True
        return False

    def dump(self):
        _claims = []
        for item in [identity.dump() for identity in self.identities]:
            _claims.extend(item)
        return _claims

    @staticmethod
    def load(data: list[dict[str, Any]]) -> 'ClaimsPrincipal':
        identities: dict[str, ClaimsIdentity] = {}
        for _data in data:
            _scheme, _identity = ClaimsIdentity.load(_data)
            if not identities.get(_scheme):
                identities[_scheme] = _identity
            else:
                identities[_scheme].add_claims(*[c for c in _identity.claims])
        return ClaimsPrincipal(*[v for v in identities.values()])


def select_primary_identity(identities: Iterable[ClaimsIdentity]):
    first_identity = None
    for identity in identities:
        if identity.is_authenticated:
            return identity
        if first_identity is None:
            first_identity = identity
    return first_identity
