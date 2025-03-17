import pytest
import json
from backend.models.Type import Type
from backend.extensions import db

class TestTypeAPI:
    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client
        """Auto-run before each test: Login and get JWT token."""
        response = client.post("/login", json={
            "username": "john@example.com",
            "password": "securepassword"
        })
        data = response.get_json()
        assert response.status_code == 200
        self.access_token = data["access_token"]

    def test_get_types_empty(self, client):
        """Test retrieving all types when none exist."""
        response = client.get("/types",headers={"Authorization": f"Bearer {self.access_token}"})
        assert response.status_code == 200
        data = response.get_json()
        if data:  # If there are existing modifiers
            assert isinstance(data, list)  # Ensure it's a list
            assert all("id" in mod and "tname" in mod for mod in data)  # Check keys
        else:  # If the database is empty
            assert data == []

    def test_create_type(self, client):
        """Test creating a new type."""
        response = client.post("/types", json={"tname": "Dessert"},headers={"Authorization": f"Bearer {self.access_token}"})
        data = response.get_json()
        if response.status_code == 201:
            assert response.status_code == 201
            assert data["message"] == "Type added successfully"
            assert data["type"] == "Dessert"
        elif response.status_code == 400:
            # Case: Type already exists
            assert data["error"] == "Type already exists"
        else:
            pytest.fail(f"Unexpected response: {response.status_code}, {data}")

    def test_create_duplicate_type(self, client):
        """Test creating a type that already exists."""
        response = client.post("/types", json={"tname": "Dessert"},headers={"Authorization": f"Bearer {self.access_token}"})  # Duplicate
        data = response.get_json()
        assert response.status_code == 400
        assert data["error"] == "Type already exists"

    def test_update_type(self, client):
        """Test updating an existing type."""
        type_id = Type.query.filter_by(tname="Dessert").first().id
        response = client.put(f"/types/{type_id}", json={"tname": "Good Dessert"},headers={"Authorization": f"Bearer {self.access_token}"})
        data = response.get_json()
        assert response.status_code == 200
        assert data["message"] == "Type updated successfully"

    def test_update_nonexistent_type(self, client):
        """Test updating a non-existent type."""
        response = client.put("/types/999", json={"tname": "Invalid"},headers={"Authorization": f"Bearer {self.access_token}"})
        assert response.status_code == 404
        assert response.get_json() == {"error": "Type not found"}

    def test_delete_type(self, client):
        """Test deleting an existing type."""
        type_id = Type.query.filter_by(tname="Good Dessert").first().id
        response = client.delete(f"/types/{type_id}",headers={"Authorization": f"Bearer {self.access_token}"})
        assert response.status_code == 200
        assert response.get_json() == {"message": "Type deleted successfully"}

    def test_delete_nonexistent_type(self, client):
        """Test deleting a non-existent type."""
        response = client.delete("/types/999",headers={"Authorization": f"Bearer {self.access_token}"})
        assert response.status_code == 404
        assert response.get_json() == {"error": "Type not found"}
