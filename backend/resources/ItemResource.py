from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from backend.extensions import db
from backend.models.Item import Item

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
