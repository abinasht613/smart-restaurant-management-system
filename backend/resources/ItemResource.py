from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from backend.extensions import db
from backend.models.Item import Item
from backend.models.Size import Size
from backend.models.Type import Type
from backend.models.ItemDetails import ItemDetails

class ItemResourceCR(Resource):
    @jwt_required()
    def post(self):
        """Add a new item"""
        data = request.json
        # Check if the item already exists (case-insensitive)
        existing_item = Item.query.filter(db.func.lower(Item.iname) == data["iname"]).first()
        if existing_item:
            return {"error": "Item already exists"}, 400  # Return error if exists
        item = Item(iname=data["iname"])
        db.session.add(item)
        db.session.commit()
        return {"message": "Item added successfully", "item": item.iname,"item_id":item.id}, 201

    @jwt_required()
    def get(self):
        """Retrieve all items"""
        items = Item.query.all()
        return [{"id": i.id, "iname": i.iname} for i in items], 200

class ItemResourceUD(Resource):
    @jwt_required()
    def put(self, item_id):
        """Update an item by ID"""
        data = request.json
        item = Item.query.get(item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404
        item.iname = data["iname"]
        db.session.commit()
        return jsonify({"message": "Item updated successfully"})

    @jwt_required()
    def delete(self, item_id):
        """Delete an item by ID"""
        item = Item.query.get(item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted successfully"})

class ItemAndItemDetails(Resource):
    @jwt_required()
    def post(self):
        """Create an item along with its variants (size, type, price, stock)."""
        data = request.json

        if "iname" not in data or "variants" not in data:
            return {"error": "Missing item name or variants"}, 400
        if data["iname"] == "":
            return {"error": "Item name cannot be empty"}, 400
        # Check if the item already exists
        existing_item = Item.query.filter_by(iname=data["iname"]).first()
        if existing_item:
            return {"error": "Item already exists"}, 400

        # Create new item
        item = Item(iname=data["iname"])
        db.session.add(item)
        db.session.flush()  # Get item.id before committing

        # Process variants
        variants_to_add = []
        for variant in data["variants"]:
            if "size_id" not in variant or "price" not in variant or "qty" not in variant:
                return {"error": "Each variant must have size_id, price, and qty"}, 400

            size = Size.query.get(variant["size_id"])
            if not size:
                return {"error": f"Size ID {variant['size_id']} not found"}, 404

            type_obj = Type.query.get(variant["type_id"]) if "type_id" in variant else None

            # Create variant entry
            item_detail = ItemDetails(
                item_id=item.id,
                size_id=variant["size_id"],
                type_id=variant.get("type_id"),
                price=variant["price"],
                qty=variant["qty"]
            )
            variants_to_add.append(item_detail)

        # Bulk insert variants
        db.session.add_all(variants_to_add)
        db.session.commit()

        return {
            "message": "Item and variants added successfully",
            "id": item.id,
            "name": item.iname,
            "variants": [
                {
                    "size_id": v.size_id,
                    "size": v.size.sname if v.size else None,
                    "type_id": v.type_id,
                    "type": v.type.tname if v.type else None,
                    "price": v.price,
                    "stock": v.qty
                }
                for v in variants_to_add
            ]
        }, 201
    