from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from backend.extensions import db
from backend.models.Size import Size

class SizeListResource(Resource):
    @jwt_required()
    def get(self):
        """Retrieve all sizes"""
        sizes = Size.query.all()
        return [{"id": s.id, "sname": s.sname} for s in sizes], 200

    @jwt_required()
    def post(self):
        """Add a new size"""
        data = request.json
        if "sname" not in data:
            return {"error": "Missing sname"}, 400
        # Check if the size already exists
        existing_size = Size.query.filter_by(sname=data["sname"]).first()
        if existing_size:
            return {"error": "Size already exists"}, 409  # HTTP 409 Conflict
        size = Size(sname=data["sname"])
        db.session.add(size)
        db.session.commit()
        return {"message": "Size added successfully", "size": size.sname,"id":size.id}, 201

class SizeResource(Resource):
    @jwt_required()
    def put(self, size_id):
        """Update a size by ID"""
        data = request.json
        if "sname" not in data:
            return {"error": "Missing sname"}, 400
        size = Size.query.get(size_id)
        if not size:
            return {"error": "Size not found"}, 404
        size.sname = data["sname"]
        db.session.commit()
        return {"message": "Size updated successfully"}, 200

    @jwt_required()
    def delete(self, size_id):
        """Delete a size by ID"""
        size = Size.query.get(size_id)
        if not size:
            return {"error": "Size not found"}, 404
        db.session.delete(size)
        db.session.commit()
        return {"message": "Size deleted successfully"}, 200
