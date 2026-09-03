# app factory 
from flask import Flask 

def create_app():
    app = Flask(__name__)

    app.config.from_object('app.config.config.Config')

    # from app.routes. import 
    # app.register_blueprint(auth_bp)
    return app
