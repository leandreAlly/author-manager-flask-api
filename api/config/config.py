class Config(object):
  DEBUG: False
  TESTING: False
  SQLALCHEMY_TRACK_MODFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/playground'

class DevelopmentConfig(Config):
   DEBUG: True
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/playground'

class TestingConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root:password@localhost:3306/playground'
  SQLALCHEMY_ECHO = False

