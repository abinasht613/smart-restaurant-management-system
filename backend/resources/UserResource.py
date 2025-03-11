from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from backend.models.User import User
from backend.extensions import db


class RegisterAPI(Resource):
    def post(self):
        data = request.get_json()
        fname = data.get("fname")
        lname = data.get("lname")
        role = data.get("role")
        username = data.get("username")
        password = data.get("password")

        if User.query.filter_by(username=username).first():
            return {"message": "User already exists"}, 400

        new_user = User(fname=fname, lname=lname, role=role, username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully"}, 201

class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return {"message": "Invalid credentials"}, 401

        access_token = create_access_token(identity={"id": user.id, "role": user.role})
        refresh_token = create_refresh_token(identity={"id": user.id, "role": user.role})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "fname": user.fname,
                "lname": user.lname,
                "role": user.role
            }
        }, 200

class RefreshTokenAPI(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return {"access_token": new_access_token}, 200

class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        print(current_user)
        # return jsonify({"message": f"Hello N/A, Role: N/A"})
        return {"message": f"Hello {current_user['id']}, Role: {current_user['role']}"}

class NotProtectedResource(Resource):
    def get(self):
        return {"message": "Hello N/A, Role: N/A"}