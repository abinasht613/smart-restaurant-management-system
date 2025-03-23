import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.create_app import create_app
from backend.extensions import socketio
# import eventlet
# eventlet.monkey_patch()  # Ensure eventlet works properly


app = create_app()

if __name__ == "__main__":
    # import eventlet
    # eventlet.monkey_patch()  # Ensure eventlet works properly
    # eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 5000)), app)
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)