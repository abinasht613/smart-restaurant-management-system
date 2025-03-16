from flask_socketio import join_room
from flask_jwt_extended import decode_token
from flask import request

def register_socket_events(socketio):
    """Register WebSocket events."""
    
    @socketio.on("connect")
    def handle_connect():
        """Handle client connections and verify JWT."""
        auth_token = request.args.get("token")  # Get JWT token from frontend
        print("A user connected.")
        if not auth_token:
            return False  # Reject connection if no token provided
        print(f"Auth token: {auth_token}")
        try:
            user_info = decode_token(auth_token)  # Decode the JWT token
            user_role = user_info.get("role")

            if user_role == "chef":
                join_room("chefs")  # Add only chefs to the "chefs" room
                print(f"Chef {user_info['id']} connected to WebSocket.")
            else:
                print(f"User {user_info['id']} is not a chef. WebSocket access denied.")

        except Exception as e:
            print(f"Invalid token: {e}")
            return False  # Reject connection if token is invalid

    @socketio.on("disconnect")
    def handle_disconnect():
        """Handle disconnections."""
        print("A user disconnected.")
