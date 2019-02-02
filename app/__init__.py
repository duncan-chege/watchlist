from flask import Flask
from .config import DevConfig   #to make our app use the new configurations
from flask_bootstrap import Bootstrap

#Initializing application

#instance_relative_config allows us to connect to the instance/folder when the app instance is created.
app = Flask(__name__, instance_relative_config = True)

#Setting up configuration
app.config.from_object(DevConfig)
app.config.from_pyfile('config.py')     #connects to the config.py file and all its contents are appended to the app.config.

# Initializing Flask Extensions
bootstrap = Bootstrap(app)

from app import views
from app import error   #import error file in __init__.py file
