from flask import Flask, jsonify
from flask_migrate import Migrate
import os
from flask_cors import CORS
from dotenv import load_dotenv
from urllib.parse import quote
from backend.routes import register_routes
from backend.extensions import db, jwt, socketio
from backend.sockets import register_socket_events

def load_config(app, config_name):
    """Load configuration based on the environment."""
    load_dotenv()
    
    DB_CONFIG = {
        "DB_NAME": os.getenv("POSTGRES_DB"),
        "DB_USER": os.getenv("POSTGRES_USER"),
        "DB_PASSWORD": quote(os.getenv("POSTGRES_PASSWORD")),
        "DB_HOST": os.getenv("POSTGRES_HOST", "db"),
        "DB_PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
    
    app.config.update({
        "SQLALCHEMY_DATABASE_URI": f"postgresql://{DB_CONFIG['DB_USER']}:{DB_CONFIG['DB_PASSWORD']}@{DB_CONFIG['DB_HOST']}:{DB_CONFIG['DB_PORT']}/{DB_CONFIG['DB_NAME']}",
        "SECRET_KEY": os.getenv("SECRET_KEY", "your_secret_key"),
        "JWT_SECRET_KEY": os.getenv("JWT_SECRET_KEY", "your_jwt_secret"),
        "JWT_ACCESS_TOKEN_EXPIRES": 86400,
        "JWT_REFRESH_TOKEN_EXPIRES": 86400,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })
    
    if config_name == "testing":
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "connect_args": {"options": "-c timezone=Asia/Kolkata"}
        }

def initialize_extensions(app):
    """Initialize Flask extensions."""
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*", async_mode="eventlet", websocket=True)
    Migrate(app, db)

def create_app(config_name="production"):
    """Create and configure the Flask app."""
    app = Flask(__name__)
    
    load_config(app, config_name)
    initialize_extensions(app)
    register_routes(app)
    # register_socket_events(socketio)
    
    CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"message": "Route not found: 404"})
    
    return app
