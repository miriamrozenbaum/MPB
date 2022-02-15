from flask.json import jsonify
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from flask import Flask, config, redirect
import os
from src.auth import auth
from src.blog import posts
from src.database import db
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from
from src.config.swagger import template, swagger_config


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),


            SWAGGER={
                'title': "Mobileye Private Blog (MPB) API",
                'uiversion': 3
            }
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)
    db.create_all()
    
    app.register_blueprint(auth)
    app.register_blueprint(posts)
    JWTManager(app)
    Swagger(app, config=swagger_config, template=template)

   
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'Not found'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong, we are working on it'}), HTTP_500_INTERNAL_SERVER_ERROR

    @app.errorhandler(HTTP_401_UNAUTHORIZED)
    def handle_404(e):
        return jsonify({'error': 'Unauthorized'}), HTTP_401_UNAUTHORIZED

    @app.errorhandler(HTTP_400_BAD_REQUEST)
    def handle_500(e):
        return jsonify({'error': 'Invalid request'}), HTTP_400_BAD_REQUEST

    return app
