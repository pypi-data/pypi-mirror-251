from pydantic import BaseModel


class AccessTokenResponse(BaseModel):
    token_type: str = "Bearer"
    access_token: str
    expires_in: int
    refresh_token: str
