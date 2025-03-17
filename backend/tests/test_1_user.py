import json
import pytest

class TestUserAPI:
    """Test suite for authentication endpoints."""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        """Setup method to run before every test."""
        self.client = client
        self.register_user()

    def register_user(self):
        """Helper method to register a user for testing."""
        self.client.post("/register", json={
            "fname": "John",
            "lname": "Doe",
            "role": "cashier",
            "username": "john@example.com",
            "password": "securepassword"
        })

    def test_register(self):
        """Test user registration."""
        response = self.client.post("/register", json={
            "fname": "Jane",
            "lname": "Doe",
            "role": "manager",
            "username": "jane@example.com",
            "password": "securepassword"
        })
        data = response.get_json()
        assert response.status_code == 201
        assert data["message"] == "User registered successfully"

    def test_login(self):
        """Test user login and JWT token retrieval."""
        response = self.client.post("/login", json={
            "username": "john@example.com",
            "password": "securepassword"
        })
        data = response.get_json()

        assert response.status_code == 200
        assert "access_token" in data
        assert "refresh_token" in data
        return data["access_token"], data["refresh_token"]
        # access_token = data["access_token"]
        # refresh_token = data["refresh_token"]

        # assert isinstance(access_token, str)  # Ensure token is a string
        # assert isinstance(refresh_token, str)
    

    def test_refresh_token(self):
        """Test refreshing access token."""
        _, refresh_token = self.test_login()

        response = self.client.post("/refresh", headers={"Authorization": f"Bearer {refresh_token}"})
        data = response.get_json()

        assert response.status_code == 200
        assert "access_token" in data

    def test_protected_resource(self):
        """Test protected route requiring JWT authentication."""
        access_token, _ = self.test_login()

        response = self.client.get("/protected", headers={"Authorization": f"Bearer {access_token}"})
        data = response.get_json()

        assert response.status_code == 200
        assert "Hello" in data["message"]

    def test_not_protected_resource(self):
        """Test public (not protected) route."""
        response = self.client.get("/not-protected")
        data = response.get_json()

        assert response.status_code == 200
        assert "Hello N/A" in data["message"]
