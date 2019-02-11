from flask import Flask
from flask_bootstrap import Bootstrap
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager  #Import login manager class
from flask_uploads import UploadSet,configure_uploads,IMAGES    #import the UploadSet class that defines what type of file we are uploading
from flask_mail import Mail     #import the the Mail class from the flask_mail extension
from flask_simplemde import SimpleMDE

login_manager = LoginManager()  #create an instance of that class
login_manager.session_protection= 'strong'    #attribute provides different security levels and by setting it to strong will monitor the changes in a user's request header and log the user out.
login_manager.login_view = 'auth.login'     #prefix the login endpoint with the blueprint name because it is located inside a blueprint.

bootstrap = Bootstrap()
db = SQLAlchemy()

bootstrap = Bootstrap()

photos = UploadSet('photos',IMAGES)     #pass in a name and the Type of file to upload which is an Image.

mail = Mail()

simple = SimpleMDE()

def create_app(config_name):

    app = Flask(__name__)

    # Creating the app configurations
    app.config.from_object(config_options[config_name])

    # Initializing flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # setting config
    from .request import configure_request
    configure_request(app)

    #registering our blueprint instance in create_app function
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/authenticate')  #pass in a url_prefix argument that will add a prefix to all the routes registered with that blueprint

    #configure uploadSet
    configure_uploads(app,photos)       #pass in the app instance and the UploadSet instance.

    mail.init_app(app)      #initializes mail settings from application settings

    simple.init_app(app)        #instantiate the plugin simpleMDE
    
    return app