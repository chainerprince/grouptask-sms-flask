from flask import Flask
from config import config


# Create instance of packages


# Factory application
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # Initialize the config object
    config[config_name].init_app(app)
    
    # Initialize all instances
    
    
    # Attach blueprints
    from smsapp.auth import auth as auth_blueprint
    from smsapp.main import main as main_blueprint
    
    # Register blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint)
    
    
    # Return application factory
    return app