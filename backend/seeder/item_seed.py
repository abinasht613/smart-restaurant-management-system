import sys
import os
# Ensure backend module is discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from backend.extensions import db
from backend.create_app import create_app
from backend.models.Item import Item
from backend.models.Size import Size
from backend.models.Type import Type
from backend.models.ItemDetails import ItemDetails

class Seeder:
    def __init__(self):
        """Initialize the database connection."""
        self.app = create_app()
        self.items = []
        self.sizes = []
        self.types = []
        self.item_details = []

    def seed_data(self):
        """Seed the database with initial data."""
        with self.app.app_context():
            db.create_all()

            if self._is_seeded():
                print("Items already seeded!")
                return
            
            self._seed_items()
            self._seed_sizes()
            self._seed_types()
            self._seed_item_details()

            db.session.commit()
            print("Database successfully seeded!")

    def _is_seeded(self):
        """Check if the database is already seeded."""
        return Item.query.first() is not None

    def _seed_items(self):
        """Seed items into the database."""
        self.items = [
            Item(iname="Margherita Pizza"),
            Item(iname="Pepperoni Pizza"),
            Item(iname="BBQ Chicken Pizza"),
            Item(iname="Caesar Salad"),
            Item(iname="Veggie Burger"),
            Item(iname="French Fries"),
        ]
        db.session.add_all(self.items)

    def _seed_sizes(self):
        """Seed sizes into the database."""
        self.sizes = [
            Size(sname="Small"),
            Size(sname="Medium"),
            Size(sname="Large"),
        ]
        db.session.add_all(self.sizes)

    def _seed_types(self):
        """Seed types into the database."""
        self.types = [
            Type(tname="Veg"),
            Type(tname="Non-Veg"),
        ]
        db.session.add_all(self.types)

    def _seed_item_details(self):
        """Seed item details including prices and stock."""
        self.item_details = [
            ItemDetails(item_id=1, size_id=1, type_id=1, price=8.99, qty=10),  # Veg Small Margherita
            ItemDetails(item_id=1, size_id=2, type_id=1, price=10.99, qty=10), # Veg Medium Margherita
            ItemDetails(item_id=2, size_id=3, type_id=2, price=12.99, qty=10), # Non Veg Large Pepperoni
            ItemDetails(item_id=4, size_id=1, type_id=1, price=6.99, qty=10),  # Veg Small Caesar Salad
            ItemDetails(item_id=5, size_id=2, type_id=1, price=9.99, qty=10),  # Veg Medium Veggie Burger
        ]
        db.session.add_all(self.item_details)

if __name__ == "__main__":
    Seeder().seed_data()
