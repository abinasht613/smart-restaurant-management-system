import pytest
import json
from backend.models.Modifier import Modifier
from backend.extensions import db

class TestModifierAPI:

    @pytest.fixture(autouse=True)
    def setup(self, client):
        """Auto-run before each test: Login and get JWT token."""
        response = client.post("/login", json={
            "username": "john@example.com",
            "password": "securepassword"
        })
        data = response.get_json()
        assert response.status_code == 200
        self.access_token = data["access_token"]

        # Cleanup database before each test
        # db.session.query(Modifier).delete()
        # db.session.commit()

    def test_get_modifiers_empty(self, client):
        """Test retrieving modifiers when none exist."""
        response = client.get("/modifiers", headers={"Authorization": f"Bearer {self.access_token}"})
        assert response.status_code == 200
        data = response.get_json()
        if data:  # If there are existing modifiers
            assert isinstance(data, list)  # Ensure it's a list
            assert all("id" in mod and "mname" in mod and "price" in mod for mod in data)  # Check keys
        else:  # If the database is empty
            assert data == []

    def test_create_modifier(self, client):
        """Test creating a new modifier."""
        response = client.post("/modifiers", headers={"Authorization": f"Bearer {self.access_token}"},
                               json={"mname": "Extra Cheese", "price": 1.5})
        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "Modifier added successfully"
        assert data["modifier"] == "Extra Cheese"

    def test_create_modifier_missing_fields(self, client):
        """Test creating a modifier with missing fields."""
        response = client.post("/modifiers", headers={"Authorization": f"Bearer {self.access_token}"},
                               json={"mname": "No Price"})
        assert response.status_code == 400
        assert response.get_json() == {"error": "Missing required fields"}

    def test_update_modifier(self, client):
        """Test updating an existing modifier."""
        mod_id = Modifier.query.filter_by(mname="Extra Cheese").first().id

        # Update the modifier
        response = client.put(f"/modifiers/{mod_id}", headers={"Authorization": f"Bearer {self.access_token}"},
                              json={"mname": "Extra Cheese Updated", "price": 2.0})
        assert response.status_code == 200
        assert response.get_json() == {"message": "Modifier updated successfully"}

    def test_update_modifier_not_found(self, client):
        """Test updating a non-existent modifier."""
        response = client.put("/modifiers/999", headers={"Authorization": f"Bearer {self.access_token}"},
                              json={"mname": "Non-existent", "price": 3.0})
        assert response.status_code == 404
        assert response.get_json() == {"error": "Modifier not found"}

    def test_delete_modifier(self, client):
        """Test deleting an existing modifier."""
        mod_id = Modifier.query.filter_by(mname="Extra Cheese Updated").first().id

        # Delete the modifier
        response = client.delete(f"/modifiers/{mod_id}", headers={"Authorization": f"Bearer {self.access_token}"})
        assert response.status_code == 200
        assert response.get_json() == {"message": "Modifier deleted successfully"}

    def test_delete_modifier_not_found(self, client):
        """Test deleting a non-existent modifier."""
        response = client.delete("/modifiers/999", headers={"Authorization": f"Bearer {self.access_token}"})
        assert response.status_code == 404
        assert response.get_json() == {"error": "Modifier not found"}
