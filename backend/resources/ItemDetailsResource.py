from flask import request
from flask_restful import Resource
from backend.extensions import db
from backend.models.ItemDetails import ItemDetails
from backend.models.Item import  Item
from backend.models.Size import Size 
from backend.models.Type import Type

class ItemDetailsResource(Resource):
    def get(self, item_detail_id=None):
        """Fetch all item details or a specific item detail by ID."""
        if item_detail_id:
            item_detail = ItemDetails.query.get(item_detail_id)
            if not item_detail:
                return {"error": "Item detail not found"}, 404
            return {
                "id": item_detail.id,
                "item_id": item_detail.item_id,
                "size_id": item_detail.size_id,
                "type_id": item_detail.type_id,
                "price": item_detail.price,
                "qty": item_detail.qty
            }, 200

        # Return all item details
        item_details = ItemDetails.query.all()
        return [
            {
                "id": item.id,
                "item_id": item.item_id,
                "size_id": item.size_id,
                "type_id": item.type_id,
                "price": item.price,
                "qty": item.qty
            }
            for item in item_details
        ], 200

    def post(self):
        """Create a new item detail."""
        data = request.json
        if "item_id" not in data or "size_id" not in data or "type_id" not in data or "price" not in data or "qty" not in data:
            return {"error": "Missing item_id/size_id/type_id/price/qty"}, 400
        item = Item.query.get(data["item_id"])
        size = Size.query.get(data["size_id"])
        type_obj = Type.query.get(data["type_id"])

        if not item or not size or not type_obj:
            return {"error": "Invalid item_id, size_id, or type_id"}, 400
        
        item_detail = ItemDetails.query.filter_by(item_id=data["item_id"], size_id=data["size_id"], type_id=data["type_id"]).first()
        if item_detail:
            item_detail.price = data.get("price", item_detail.price)
            item_detail.qty = data.get("qty", item_detail.qty)
            db.session.commit()
            return {"message": "Item detail updated successfully"}, 200
        else: 
            new_item_detail = ItemDetails(
                item_id=data["item_id"],
                size_id=data["size_id"],
                type_id=data["type_id"],
                price=data["price"],
                qty=data["qty"]
            )
            db.session.add(new_item_detail)
            db.session.commit()

            return {
                "message": "Item detail added successfully",
                "id": new_item_detail.id
            }, 201

    def put(self, item_detail_id):
        """Update an existing item detail."""
        item_detail = ItemDetails.query.get(item_detail_id)
        if not item_detail:
            return {"error": "Item detail not found"}, 404

        data = request.json
        item_detail.price = data.get("price", item_detail.price)
        item_detail.qty = data.get("qty", item_detail.qty)

        db.session.commit()
        return {"message": "Item detail updated successfully"}, 200

    def delete(self, item_detail_id):
        """Delete an item detail."""
        item_detail = ItemDetails.query.get(item_detail_id)
        if not item_detail:
            return {"error": "Item detail not found"}, 404

        db.session.delete(item_detail)
        db.session.commit()
        return {"message": "Item detail deleted successfully"}, 200
