class BaseConfig():
    DEBUG = True
    # SECRET_KEY = open('path/to/secret/key').read()

class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False