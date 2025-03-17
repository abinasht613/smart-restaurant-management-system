import json
import pytest
from backend.models.Item import Item
from backend.extensions import db

# @pytest.mark.usefixtures("app", "client", "auth_headers")
class TestItemAPI:
    
    @pytest.fixture(autouse=True)
    def test_login(self,client):
        """Test user login and JWT token retrieval."""
        response = client.post("/login", json={
            "username": "john@example.com",
            "password": "securepassword"
        })
        data = response.get_json()

        assert response.status_code == 200
        assert "access_token" in data
        assert "refresh_token" in data
        return data["access_token"], data["refresh_token"]

    # def setup_and_teardown(self):
    #     """Auto-run before and after each test (DB setup & cleanup)."""
    #     db.session.query(Item).delete()  # Clear previous test data
    #     db.session.commit()

    def test_create_item(self, client, test_login):
        """Test access token."""
        access_token, _ = test_login
        """Test creating a new item."""
        response = client.post("/items", headers={"Authorization": f"Bearer {access_token}"},json={"iname": "Pizza"})
        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "Item added successfully"
        assert data["item"] == "Pizza"

    def test_get_items(self, client, test_login):
        access_token, _ = test_login
        """Test retrieving all items."""
        client.post("/items", json={"iname": "Burger"}, headers={"Authorization": f"Bearer {access_token}"})  # Add an item
        
        response = client.get("/items", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200
        data = response.get_json()
        
        assert isinstance(data, list)
        assert len(data) > 0
        assert any(item["iname"] == "Burger" for item in data)

    def test_update_item(self, client, test_login):
        access_token, _ = test_login
        """Test updating an item."""
        response = client.post("/items", json={"iname": "Fries"},headers={"Authorization": f"Bearer {access_token}"})
        item_id = response.get_json()["item_id"]
        
        response = client.put(f"/items/{item_id}", json={"iname": "Large Fries"}, headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Item updated successfully"
        
        updated_item = Item.query.get(item_id)
        assert updated_item.iname == "Large Fries"

    def test_delete_item(self, client, test_login):
        access_token, _ = test_login
        """Test deleting an item."""
        response = client.post("/items", json={"iname": "Soda"}, headers={"Authorization": f"Bearer {access_token}"})
        item_id = response.get_json()["item_id"]
        
        response = client.delete(f"/items/{item_id}", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Item deleted successfully"
        
        assert Item.query.get(item_id) is None
