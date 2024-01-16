from dataclasses import dataclass

from iFastApi.mode import BaseModel
from pydantic import Field
from iFastApi.api.BaseDataClass import BaseDataClass


@dataclass
class AccountDc(BaseDataClass):
    account: str
    password: str
    identity: str = None
    u_id: str = None
    id: int = None


class LoginMode(BaseModel):
    """登录模型"""
    account: str = Field(..., max_length=11, min_length=5)
    password: str = Field(..., min_length=6, max_length=20)


class RegisterMode(LoginMode):
    """注册模型"""
    identity: str = Field(...)
