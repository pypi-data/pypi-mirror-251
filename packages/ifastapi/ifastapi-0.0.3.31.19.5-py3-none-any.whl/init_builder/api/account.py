import asyncio

from iFastApi import BaseRoute
from iFastApi.api.RouteInfo import RouteInfo
from iFastApi.utils.iResponse import Success, JSONResponse

from db.account import Account as dbAccount
from model.account import LoginMode, RegisterMode, AccountDc


class Account(BaseRoute):
    def __init__(self, prefix=None):
        super().__init__(prefix)
        self.routers = [
            RouteInfo('/login', self.login),
            RouteInfo('/register', self.register, verify_auth=['ADMIN']),
            RouteInfo('/test_async_insert', self.async_insert)  # 异步测试
        ]
        self.db = dbAccount

    @staticmethod
    async def insert_data():
        await asyncio.sleep(1)
        print("Data inserted")

    async def async_insert(self):
        asyncio.create_task(self.insert_data())
        return Success()

    def login(self, response: LoginMode) -> JSONResponse:
        account_dc = self.db.check_login(AccountDc(**response.dict()))
        return Success(data=account_dc)

    def register(self, response: RegisterMode) -> JSONResponse:
        account_dc = self.db.create_account(AccountDc(**response.dict()))
        return Success(data=account_dc.dict)
