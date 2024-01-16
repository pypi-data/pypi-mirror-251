from datetime import timedelta


class ServerConf:
    ORIGINS = ["*"]
    EVO_LABEL = '[测试环境]'
    EVO = 'testing'
    POWER_KEY = 'identity'
    SERVER_CONFIG = {
        "app": "main:IFastAPI.app",
        "host": "localhost",
        "port": 5000,
        "reload": True,
        # "workers": 3,
    }
    DB_CONFIG = {
        "dialect": 'mysql',
        "driver": 'pymysql',
        "username": 'username',
        "password": 'password',
        "host": 'host',
        "port": 'port',
        "database": 'db_serverwatch'
    }
    REDIS_DB = {
        "host": "host",
        "port": 1000,
        "password": 'password',
        "db": 1,
    }
    SQLALCHEMY_DATABASE_URI = "{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}?charset=utf8".format(**DB_CONFIG)
    ACCESS_TOKEN_EXPIRES = timedelta(minutes=60 * 10)
    PARAM_TRANSLATE = {}
