import uuid

from fastapi import Request, Response

from fastapi_identity.core.claims import ClaimsPrincipal


class HttpContext:
    def __init__(self, request: Request, response: Response):
        self._request = request
        self._response = response

    @property
    def request(self) -> Request:
        return self._request

    @property
    def response(self) -> Response:
        return self._response

    @property
    def user(self) -> ClaimsPrincipal:
        return self.request.user

    async def authenticate(self, scheme: str):
        pass

    async def sign_in(self, principal: ClaimsPrincipal):
        self.response.set_cookie("fastapiidentityauth.persistent", str(uuid.uuid4()))

    async def sign_out(self):
        self.response.delete_cookie("fastapiidentityauth.persistent")
