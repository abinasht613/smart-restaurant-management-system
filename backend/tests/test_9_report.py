import pytest
import json
from backend.extensions import db
from backend.models.Item import Item
from backend.models.ItemDetails import ItemDetails
from backend.models.Order import Order
from backend.models.OrderDetails import OrderDetails
from backend.models.Size import Size
from datetime import datetime, timedelta

class TestReportAPI:
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


    def test_get_reports(self, client):
        """Test retrieving reports with sample orders."""
        response = client.get("/reports",headers={"Authorization": f"Bearer {self.access_token}"})
        data = response.get_json()

        assert response.status_code == 200

        # 🔹 Handle missing keys gracefully
        assert "peak_hours" in data, "Missing 'peak_hours' key in response"
        assert "popular_items" in data, "Missing 'popular_items' key in response"
        assert "sales_trends" in data, "Missing 'sales_trends' key in response"

         # 🔹 Validate "peak_hours"
        assert isinstance(data["peak_hours"], list)
        assert len(data["peak_hours"]) > 0  # Ensure data exists
        for hour_data in data["peak_hours"]:
            assert "hour" in hour_data
            assert "total_orders" in hour_data
            assert isinstance(hour_data["hour"], str)
            assert isinstance(hour_data["total_orders"], int)
        
        # 🔹 Validate "popular_items"
        assert isinstance(data["popular_items"], list)
        assert len(data["popular_items"]) > 0  # Ensure data exists
        for item_data in data["popular_items"]:
            assert "item" in item_data
            assert "quantity" in item_data
            assert isinstance(item_data["item"], str)
            assert isinstance(item_data["quantity"], int)

        # 🔹 Validate "sales_trends"
        assert isinstance(data["sales_trends"], list)
        assert len(data["sales_trends"]) > 0  # Ensure data exists
        for trend_data in data["sales_trends"]:
            assert "date" in trend_data
            assert "total_sales" in trend_data
            assert isinstance(trend_data["date"], str)
            assert isinstance(trend_data["total_sales"], float)