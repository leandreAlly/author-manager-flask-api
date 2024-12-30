class Config(object):
  DEBUG: False
  TESTING: False
  SQLALCHEMY_TRACK_MODFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/playground'

class DevelopmentConfig(Config):
   DEBUG: True
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/playground'
   SECRET_KEY= 'your_secured_key_here'
   SECURITY_PASSWORD_SALT= 'your_security_password_here'
   MAIL_DEFAULT_SENDER= 'your_email_address'
   MAIL_SERVER= 'email_providers_smtp_address'
   MAIL_PORT= 'mail port'
   MAIL_USERNAME= 'your_email_address'
   MAIL_PASSWORD= 'your_email_password'
   MAIL_USE_TLS= False
   MAIL_USE_SSL= True


class TestingConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root:password@localhost:3306/playground'
  SQLALCHEMY_ECHO = False

