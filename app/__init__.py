# app factory 
from flask import Flask 

def create_app():
    #create the app
    app = Flask(__name__)

    #add configuration
    app.config.from_object('app.config.config.Config')

    #register blueprints
    # from app.routes. import 
    # app.register_blueprint(auth_bp)

    #register db teardown
    from app.db.init_db import close_db
    app.teardown_appcontext(close_db)
    return app
