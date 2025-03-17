from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from backend.models.Item import Item
from backend.extensions import db

class MenuResource(Resource):
    @jwt_required(optional=True)  # Allow public access too
    def get(self):
        """Retrieve menu with items, sizes, and types."""
        items = Item.query.all()

        menu = []
        for item in items:
            item_data = {
                "id": item.id,
                "name": item.iname,
                "variants": []
            }

            for detail in item.details:
                variant = {
                    "size_id": detail.size_id,
                    "size": detail.size.sname if detail.size else None,
                    "type_id": detail.type_id,
                    "type": detail.type.tname if detail.type else None,
                    "price": detail.price,
                    "stock": detail.qty
                }
                item_data["variants"].append(variant)

            menu.append(item_data)

        return (menu), 200
