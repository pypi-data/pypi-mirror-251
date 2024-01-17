"""
from fastapi_identity import AuthenticationMiddleware, BearerAuthenticationBackend

app = FastAPI()
app.add_middleware(AuthenticationMiddleware, backend=BearerAuthenticationBackend())


"""

import json
import re
from abc import abstractmethod
from re import Pattern
from typing import Union, Optional, Callable, List

from fastapi import Request
from fastapi.security import OAuth2PasswordBearer, APIKeyCookie
from jose import jwt
from jose.exceptions import JWTClaimsError, JWTError, ExpiredSignatureError
from starlette.authentication import AuthenticationError
from starlette.datastructures import URL
from starlette.requests import HTTPConnection
from starlette.responses import Response, PlainTextResponse
from starlette.types import ASGIApp, Scope, Receive, Send

from fastapi_identity.core.claims import ClaimsPrincipal


class AuthToken:
    def __init__(self, token: dict):
        self.token = token

    @property
    def iss(self):
        return self.token.get('iss')

    @property
    def sub(self):
        return self.token.get('sub')

    @property
    def aud(self):
        return self.token.get('aud')

    @property
    def exp(self):
        return self.token.get('exp')

    @property
    def nbf(self):
        return self.token.get('nbf')

    @property
    def iat(self):
        return self.token.get('iat')

    @property
    def jti(self):
        return self.token.get('jti')

    @property
    def claims(self):
        return self.token.get('claims')


class TokenValidationParameters:
    def __init__(
            self,
            *,
            verify_signature: bool = True,
            verify_aud: bool = True,
            verify_iat: bool = True,
            verify_exp: bool = True,
            verify_nbf: bool = True,
            verify_iss: bool = True,
            verify_sub: bool = True,
            verify_jti: bool = True,
            verify_at_hash: bool = True,
            require_aud: bool = True,
            require_iat: bool = False,
            require_exp: bool = True,
            require_nbf: bool = False,
            require_iss: bool = True,
            require_sub: bool = True,
            require_jti: bool = False,
            require_at_hash: bool = False,
            leeway: int = 0
    ):
        self.verify_signature = verify_signature
        self.verify_aud = verify_aud
        self.verify_iat = verify_iat
        self.verify_exp = verify_exp
        self.verify_nbf = verify_nbf
        self.verify_iss = verify_iss
        self.verify_sub = verify_sub
        self.verify_jti = verify_jti
        self.verify_at_hash = verify_at_hash
        self.require_aud = require_aud
        self.require_iat = require_iat
        self.require_exp = require_exp
        self.require_nbf = require_nbf
        self.require_iss = require_iss
        self.require_sub = require_sub
        self.require_jti = require_jti
        self.require_at_hash = require_at_hash
        self.leeway = leeway

    def dump(self):
        return self.__dict__


class AuthenticationBackend:
    def __init__(
            self,
            scheme: Union[OAuth2PasswordBearer, APIKeyCookie],
            secret: str,
            token_validation_parameters: Optional[TokenValidationParameters] = None
    ):
        self._scheme = scheme
        self._secret = secret
        self._token_validation_parameters = token_validation_parameters or TokenValidationParameters()

    async def authenticate(self, request: Request) -> ClaimsPrincipal:
        token = await self._scheme(request)
        if not token:
            raise AuthenticationError()
        _decode_token = await self._decode_auth_token(token)
        return await self._handle(request, _decode_token)

    async def _decode_auth_token(self, token: str) -> AuthToken:
        try:
            payload = jwt.decode(
                token,
                self._secret,
                algorithms='HS256',
                options=self._token_validation_parameters.dump()
            )
            return AuthToken(payload)
        except ExpiredSignatureError as ex:
            pass
        except JWTClaimsError as ex:
            pass
        except JWTError as ex:
            pass

    @abstractmethod
    async def _handle(self, request: Request, token: AuthToken) -> ClaimsPrincipal:
        pass


class BearerAuthenticationBackend(AuthenticationBackend):
    def __init__(
            self,
            secret: str,
            tokenUrl: str
    ):
        super().__init__(
            OAuth2PasswordBearer(tokenUrl=tokenUrl, auto_error=False),
            secret
        )

    async def _handle(self, request: Request, token: AuthToken) -> ClaimsPrincipal:
        if token.claims:
            return ClaimsPrincipal.load(token.claims)
        return ClaimsPrincipal()


class CookieAuthenticationBackend(AuthenticationBackend):
    def __init__(
            self,
            secret: str,
            name: str = "FastApiIdentityAuth"
    ):
        super().__init__(
            APIKeyCookie(name=name, auto_error=False),
            secret
        )

    async def _handle(self, request: Request, token: AuthToken) -> ClaimsPrincipal:
        claims: list = []
        for cname, cval in request.cookies.items():
            if cname.startswith('__fastapiidentityauth'):
                claims.append(self._decode_cookie(cval))
        principal = ClaimsPrincipal.load(claims)
        return principal

    def _decode_cookie(self, cookie: str) -> dict:
        return json.loads(cookie)


class AuthenticationMiddleware:
    def __init__(
            self,
            app: ASGIApp,
            backend: AuthenticationBackend,
            on_error: Optional[Callable[[HTTPConnection, AuthenticationError], Response]] = None,
            allow_anonymous: Optional[List[Union[Pattern, str]]] = None,

    ) -> None:
        self.app = app
        self.backend = backend
        self.on_error = (on_error if on_error is not None else self.default_on_error)
        self.allow_anonymous = []
        for _item in allow_anonymous:
            if isinstance(_item, str):
                self.allow_anonymous.append(re.compile(_item))
            else:
                self.allow_anonymous.append(_item)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return

        request = Request(scope)
        try:
            principal = await self.backend.authenticate(request)
            scope['user'] = principal
            scope['auth'] = principal and principal.identity.is_authenticated
        except AuthenticationError as exc:
            if not self.__url_is_exempt(request.url):
                response = self.on_error(request, exc)
                if scope["type"] == "websocket":
                    await send({"type": "websocket.close", "code": 1000})
                else:
                    await response(scope, receive, send)
                return

        await self.app(scope, receive, send)

    def __url_is_exempt(self, url: URL) -> bool:
        if not self.allow_anonymous:
            return False
        for exempt_url in self.allow_anonymous:
            if exempt_url.match(url.path):
                return True
        return False

    @staticmethod
    def default_on_error(request: Request, exc: Exception) -> Response:
        return PlainTextResponse(str(exc), status_code=401)
