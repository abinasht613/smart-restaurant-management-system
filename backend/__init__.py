from flask import Flask, jsonify
# from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_jwt_extended import JWTManager
import eventlet
import os
from flask_cors import CORS
from dotenv import load_dotenv
from urllib.parse import quote
# from flask_restful import Api
from backend.routes import register_routes
from backend.extensions import db, jwt, socketio

def create_app(config_name="production"):
    # db = SQLAlchemy()
    # socketio = SocketIO(cors_allowed_origins="*")  # Enable WebSockets


    # Load environment variables from .env
    load_dotenv()
    # Access environment variables
    DB_NAME                     = os.getenv("POSTGRES_DB")
    DB_USER                     = os.getenv("POSTGRES_USER")
    DB_PASSWORD                 = quote(os.getenv("POSTGRES_PASSWORD"))
    DB_HOST                     = os.getenv("POSTGRES_HOST", "db")  # Default host is 'db' (service name in Docker Compose)
    DB_PORT                     = os.getenv("POSTGRES_PORT", "5432")  # Default port is 5432
    FLASK_ENV                   = os.getenv("FLASK_ENV")
    SECRET_KEY                  = os.getenv("SECRET_KEY", "your_secret_key")
    JWT_SECRET_KEY              = os.getenv("JWT_SECRET_KEY", "your_jwt_secret")
    JWT_ACCESS_TOKEN_EXPIRES    = 86400  # 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES   = 86400  # 1 day
    app = Flask(__name__)
    # app.config.from_object("config.Config") # Load configurations from config.py file


    # Set the configuration for the app based on the passed environment
    if config_name == "testing":
        print("Using Testing Config start")
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        app.config['SECRET_KEY'] = SECRET_KEY
        app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
        app.config['JWT_REFRESH_TOKEN_EXPIRES'] = JWT_REFRESH_TOKEN_EXPIRES
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        print("Using Testing Config end")
    elif config_name == "production":
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        app.config['SECRET_KEY'] = SECRET_KEY
        app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
        app.config['JWT_REFRESH_TOKEN_EXPIRES'] = JWT_REFRESH_TOKEN_EXPIRES
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Initialize CORS, Database, and other app-level components
    CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})  # Enable CORS for the whole app


    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, async_mode="eventlet")
    Migrate(app, db)

    # Register Routes
    register_routes(app)

    # from backend.routes  import item_routes, item_details_routes, user_routes, type_routes, size_routes, modifier_routes, report_routes, order_routes
   
    # app.register_blueprint(item_routes.bp)
    # app.register_blueprint(item_details_routes.bp)
    # app.register_blueprint(user_routes.bp)
    # app.register_blueprint(type_routes.bp)
    # app.register_blueprint(size_routes.bp)
    # app.register_blueprint(modifier_routes.bp)
    # app.register_blueprint(report_routes.bp)
    # app.register_blueprint(order_routes.bp)
        

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"message": "Route not found: 404"})

    return app