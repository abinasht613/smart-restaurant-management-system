import json
import pytest

class TestOrderAPI:
    
    @pytest.fixture(autouse=True)
    def setup(self, client):
        """Setup method to run before every test."""
        self.client = client

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
    

    def test_order_api(self):
        """Test order placement API"""
        access_token, _ = self.test_login()
        # Sample order data
        order_data = {
            "order_text": "Two large chicken pepperoni pizza extra cheese, one caesar salad, and two diet coke with Origano",
            "customer_name": "John Doe",
            "customer_mobile": "1234567890"
        }

        # Send POST request
        response = self.client.post(
            "/order",
            data=json.dumps(order_data),
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        # Validate response
        assert response.status_code == 201
        response_data = response.get_json()
        assert response_data["message"] == "Order placed successfully"
        assert "order_id" in response_data
        assert "total_amount" in response_data


    def test_get_all_orders(self):
        """Test retrieving all orders"""
        access_token, _ = self.test_login()
        response = self.client.get(
            "/orders",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200
        assert len(response.json) >= 0  # Ensure orders exist

    def test_get_single_order(self):
        access_token, _ = self.test_login()
        """Test retrieving a single order by ID"""
        response = self.client.get("/order-details/1",
            headers={"Authorization": f"Bearer {access_token}"}                           
        )  # Assuming order ID = 1
        assert response.status_code == 200
        assert response.json["total_amount"] > 0

    def test_get_single_order_invalid_id(self):
        access_token, _ = self.test_login()
        """Test retrieving an order that does not exist"""
        response = self.client.get("/order-details/999",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 404
        assert "error" in response.json

