from starlette.types import ASGIApp


class AuthorizationBackend:
    pass


class AuthorizationMiddleware:
    def __init__(
            self,
            app: ASGIApp,

    ) -> None:
        self.app = app
