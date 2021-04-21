import os


class Config():
    DEBUG = os.getenv('FLASK_DEBUG', default=False)
    ENV = os.getenv('FLASK_ENV', default='production')
    SECRET_KEY = os.getenv('SECRET_KEY')

    ALEPH_API_KEY = os.getenv('ALEPH_API_KEY')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    SECRET_KEY = 'devsecrets'


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'testing'

    ALEPH_API_KEY = ''
    AWS_ACCESS_KEY_ID = 'testing'
    AWS_BUCKET_NAME = 'samples'
    AWS_SECRET_ACCESS_KEY = 'testing'
    AWS_REGION_NAME = 'testing'
