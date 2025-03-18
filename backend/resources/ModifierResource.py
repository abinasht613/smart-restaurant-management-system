from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from backend.extensions import db
from backend.models.Modifier import Modifier

class ModifierListResource(Resource):
    @jwt_required()
    def get(self):
        """Retrieve all modifiers"""
        modifiers = Modifier.query.all()
        return [{"id": m.id, "mname": m.mname, "price": m.price} for m in modifiers], 200

    @jwt_required()
    def post(self):
        """Add a new modifier"""
        data = request.json
        if "mname" not in data or "price" not in data:
            return {"error": "Missing required fields"}, 400
        modifier = Modifier(mname=data["mname"], price=data["price"])
        db.session.add(modifier)
        db.session.commit()
        return {"message": "Modifier added successfully", "modifier": {
                "id": modifier.id,
                "name": modifier.mname,
                "price": modifier.price
            }}, 201

class ModifierResource(Resource):
    @jwt_required()
    def put(self, modifier_id):
        """Update an existing modifier"""
        data = request.json
        modifier = Modifier.query.get(modifier_id)
        if not modifier:
            return {"error": "Modifier not found"}, 404
        if "mname" in data:
            modifier.mname = data["mname"]
        if "price" in data:
            modifier.price = data["price"]
        if "mname" not in data and "price" not in data:
            return {"error": "mnane or price not found"}, 404
        db.session.commit()
        return {"message": "Modifier updated successfully"}, 200

    @jwt_required()
    def delete(self, modifier_id):
        """Delete a modifier"""
        modifier = Modifier.query.get(modifier_id)
        if not modifier:
            return {"error": "Modifier not found"}, 404
        db.session.delete(modifier)
        db.session.commit()
        return {"message": "Modifier deleted successfully"}, 200
