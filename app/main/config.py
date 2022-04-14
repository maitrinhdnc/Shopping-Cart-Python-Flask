import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'thma')
    DEBUG = False
    # Swagger
    RESTX_MASK_SWAGGER = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://admin:admin@localhost:5432/exercise1_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config_by_name = dict(
    dev=DevelopmentConfig
)

key = Config.SECRET_KEY
