from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_jwt_extended import decode_token
from flask import Flask, request

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*",async_mode="eventlet")  # Enable WebSockets

@socketio.on("connect")
def handle_connect():
    token = request.args.get("token")
    if not token:
        return False  # Reject connection
    
    try:
        user_data = decode_token(token)
        print(f"User {user_data['sub']} connected Flask")
    except Exception as e:
        print("Invalid token:", e)
        return False  # Reject connection


@socketio.on("disconnect")
def handle_disconnect():
    """Handle disconnections."""
    print("A user disconnected Flask.")

jwt = JWTManager()
