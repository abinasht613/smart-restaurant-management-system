from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from backend.extensions import db
from backend.models.Type import Type

class TypeListResource(Resource):
    @jwt_required()
    def get(self):
        """Retrieve all types"""
        types = Type.query.all()
        return [{"id": t.id, "tname": t.tname} for t in types], 200

    @jwt_required()
    def post(self):
        """Add a new type"""
        data = request.json
        if "tname" not in data:
            return {"error": "Missing tname"}, 400
        check_type = Type.query.filter_by(tname=data["tname"]).first()
        if check_type:
            return {"error": "Type already exists"}, 400
        type_obj = Type(tname=data["tname"])
        db.session.add(type_obj)
        db.session.commit()
        return {"message": "Type added successfully", "type": type_obj.tname,"id":type_obj.id}, 201

class TypeResource(Resource):
    @jwt_required()
    def put(self, type_id):
        """Update a type by ID"""
        data = request.json
        if "tname" not in data:
            return {"error": "Missing tname"}, 400
        type_obj = Type.query.get(type_id)
        if not type_obj:
            return {"error": "Type not found"}, 404
        type_obj.tname = data["tname"]
        db.session.commit()
        return {"message": "Type updated successfully"}, 200

    @jwt_required()
    def delete(self, type_id):
        """Delete a type by ID"""
        type_obj = Type.query.get(type_id)
        if not type_obj:
            return {"error": "Type not found"}, 404
        db.session.delete(type_obj)
        db.session.commit()
        return {"message": "Type deleted successfully"}, 200
