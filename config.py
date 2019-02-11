import os

class Config:
    '''
    General configuration parent class
    '''
    MOVIE_API_BASE_URL ='https://api.themoviedb.org/3/movie/{}?api_key={}'
    MOVIE_API_KEY = os.environ.get('MOVIE_API_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://dunyung1:iamyung1@localhost/watchlist'
    UPLOADED_PHOTOS_DEST ='app/static/photos'       #specifies the destination to where we want to store our Images. 
                                                    #The destination is to be a photos folder inside our static folder.
     
     # setting up simple mde  configurations for it to work
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True

class ProdConfig(Config):
    '''
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    pass

# class TestConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://dunyung1:iamyung1@localhost/watchlist_test'


class DevConfig(Config):
    '''
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://dunyung1:iamyung1@localhost/watchlist'


    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig,
# 'test':TestConfig
}

# email configurations
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")      #email address
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")     #password