import sys
import os
import pytest
# Ensure backend module is discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from backend import create_app
from backend.extensions import db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app("testing")  # Ensure this mode uses a test database
    with app.app_context():
        db.create_all()  # Create test tables
        yield app
        db.session.remove()
        # db.drop_all()  # Clean up after tests

@pytest.fixture
def client(app):
    """Create a test client for making requests."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()
