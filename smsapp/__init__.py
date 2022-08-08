from flask import Flask
from config import config
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy


# Create instance of packages
db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# Factory application
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # Initialize the config object
    config[config_name].init_app(app)
    
    # Initialize all instances
    db.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)
    
    # Attach blueprints
    from smsapp.auth import auth as auth_blueprint
    from smsapp.main import main as main_blueprint
    
    # Register blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint)
    
    
    # Return application factory
    return app