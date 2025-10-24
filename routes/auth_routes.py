from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name, email, password = data["name"], data["email"], data["password"]

    users = current_app.mongo.db.users
    if users.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = current_app.bcrypt.generate_password_hash(password).decode("utf-8")
    users.insert_one({"name": name, "email": email, "password": hashed_pw})

    return jsonify({"message": "✅ Registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email, password = data["email"], data["password"]

    users = current_app.mongo.db.users
    user = users.find_one({"email": email})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not current_app.bcrypt.check_password_hash(user["password"], password):
        return jsonify({"error": "Incorrect password"}), 400

    token = create_access_token(identity=str(user["_id"]), expires_delta=timedelta(hours=2))
    return jsonify({"token": token, "user": {"name": user["name"], "email": user["email"]}})
