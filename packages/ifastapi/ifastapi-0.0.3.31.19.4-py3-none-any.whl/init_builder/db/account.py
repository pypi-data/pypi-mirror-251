import uuid

from iFastApi import JWTBearer, Error, HTTPStatus
from iFastApi.db import BaseDB
from iFastApi.utils.toolfuns import encryption_md5
from sqlalchemy import Column, String, Integer

from model.account import AccountDc


class Account(BaseDB):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    u_id = Column(String(128), default=uuid.uuid4, unique=True, nullable=False)
    account = Column(String(24), unique=True, nullable=False, comment='账号')
    _password = Column('password', String(128), comment='密码')
    identity = Column(String(8), comment='身份')

    # region 验证密码
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = encryption_md5(raw)

    @staticmethod
    def verify(account, password):
        _account_ = Account.query.filter_by(account=account).first_or_404(message='账号不存在')
        if not _account_.check_password(password):
            raise Error(status_code=HTTPStatus.FORBIDDEN, message='密码错误')
        return {'u_id': _account_.u_id, 'token': JWTBearer.token({"u_id": _account_.u_id, "account": _account_.account}),
                'account': _account_.account, 'identity': _account_.identity}

    def check_password(self, raw) -> bool:
        if not self._password:
            return False
        return self._password == encryption_md5(raw)

    # endregion

    # region 创建账号
    @classmethod
    def create_account(cls, account_dc: AccountDc):
        _account_ = Account.query.filter_by(account=account_dc.account).no_one()
        _account_ = Account(**account_dc.dict)
        _account_.password = account_dc.password
        cls.db.add(_account_)
        cls.db.commit()
        account_dc.id = _account_.id
        account_dc.u_id = _account_.u_id
        return account_dc

    # endregion
    @classmethod
    def check_login(cls, account_dc: AccountDc):
        return cls.verify(account_dc.account, account_dc.password)
