# app factory 
from flask import Flask 

def create_app():
    #create the app
    app = Flask(__name__)

    #add configuration
    app.config.from_object('app.config.config.Config')

    #register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.admin import admin_bp
    from app.routes.user import user_bp
    app.register_blueprint(auth_bp) 
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)

    #register db teardown
    from app.db.init_db import close_db
    app.teardown_appcontext(close_db)
    return app
