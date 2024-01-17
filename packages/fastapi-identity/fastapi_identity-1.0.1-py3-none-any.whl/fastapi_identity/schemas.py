import datetime
from typing import Generic, Optional

from pydantic import BaseModel, EmailStr, ConfigDict, Field

from pydentity.types import GUID, TKey


class BaseRegisterUser(BaseModel):
    email: EmailStr
    password: str


class BaseResetPassword(BaseModel):
    email: EmailStr
    password: str


class BaseUser(BaseModel, Generic[TKey]):
    model_config = ConfigDict(from_attributes=True)

    concurrency_stamp: Optional[GUID] = None
    email: Optional[EmailStr] = None
    email_confirmed: bool = False
    id: TKey
    lockout_enabled: bool = True
    lockout_end: Optional[datetime.datetime] = None
    phone_number: Optional[str] = None
    phone_number_confirmed: bool = False
    security_stamp: Optional[GUID] = None
    two_factor_enabled: bool = False
    username: Optional[str] = None


class BaseCreateRole(BaseModel):
    name: str


class BaseRole(BaseModel, Generic[TKey]):
    model_config = ConfigDict(from_attributes=True)

    id: TKey
    name: Optional[str] = None
