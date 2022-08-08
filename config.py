import os

# Configuration Class
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    

    @staticmethod
    def init_app(app):
        pass

# Configuration for the app(Development or Testing)
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:pg1234@localhost/newsmsdb"

class TestingConfig(Config):
    TESTING = True
    pass

# Configuration dictionary for the defined Config Classes
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}