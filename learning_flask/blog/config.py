class Config(object):
    POSTS_PER_PAGE = 5

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///database_org.db"
    SQLALCHEMY_ECHO = True

class ProdConfig(Config):
    pass