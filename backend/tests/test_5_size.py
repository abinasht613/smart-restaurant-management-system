import pytest
from backend.models.Size import Size
from backend.extensions import db

class TestSizeAPI:
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


    def test_get_sizes_empty(self):
        """Test retrieving sizes when database is empty."""
        response = self.client.get("/sizes", headers={"Authorization": f"Bearer {self.access_token}"})
        assert response.status_code == 200
        # assert response.get_json() == []
        data = response.get_json()
        if data:  # If there are existing modifiers
            assert isinstance(data, list)  # Ensure it's a list
            assert all("id" in mod and "sname" in mod for mod in data)  # Check keys
        else:  # If the database is empty
            assert data == []

    def test_create_size(self):
        """Test creating a new size."""
        response = self.client.post("/sizes", json={"sname": "Larger"}, headers={"Authorization": f"Bearer {self.access_token}"})
        data = response.get_json()
        if response.status_code == 201:
            # Case: Successfully added
            assert data["message"] == "Size added successfully"
            assert data["size"] == "Larger"
        elif response.status_code == 400:
            # Case: Size already exists
            assert data["error"] == "Size already exists"
        else:
            pytest.fail(f"Unexpected response: {response.status_code}, {data}")

    # def test_get_sizes_populated(self):
    #     """Test retrieving sizes when database has entries."""
    #     self.client.post("/sizes", json={"sname": "Medium"}, headers={"Authorization": f"Bearer {self.access_token}"})
    #     response = self.client.get("/sizes")
    #     assert response.status_code == 200
    #     data = response.get_json()
    #     assert isinstance(data, list)
    #     assert len(data) == 1
    #     assert data[0]["sname"] == "Medium"

    def test_update_size(self):
        """Test updating an existing size."""
        size_id = Size.query.filter_by(sname="Larger").first().id

        # Update the size
        update_response = self.client.put(f"/sizes/{size_id}", json={"sname": "Extra Larger"}, headers={"Authorization": f"Bearer {self.access_token}"})
        assert update_response.status_code == 200
        assert update_response.get_json()["message"] == "Size updated successfully"

    def test_delete_size(self):
        """Test deleting a size."""
        size_id = Size.query.filter_by(sname="Extra Larger").first().id

        # Delete the size
        delete_response = self.client.delete(f"/sizes/{size_id}",headers={"Authorization": f"Bearer {self.access_token}"})
        assert delete_response.status_code == 200
        assert delete_response.get_json()["message"] == "Size deleted successfully"

