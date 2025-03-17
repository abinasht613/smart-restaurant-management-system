import pytest
import json

class TestMenuAPI:
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

    def test_get_menu(self, client):
        """Test retrieving an empty menu."""
        response = client.get("/menu",headers={"Authorization": f"Bearer {self.access_token}"})
        data = response.get_json()
        assert response.status_code == 200
        if len(data)>0:
            pass
        elif (len(data)==0):
            assert response.get_json() == []
        else:
            pass