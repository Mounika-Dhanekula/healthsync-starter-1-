from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

vital_bp = Blueprint("vital_bp", __name__)

@vital_bp.route("/", methods=["GET"])
@jwt_required()
def get_vitals():
    user_id = get_jwt_identity()
    vitals = list(current_app.mongo.db.vitals.find({"userId": user_id}))
    for v in vitals:
        v["_id"] = str(v["_id"])
    return jsonify(vitals)

@vital_bp.route("/", methods=["POST"])
@jwt_required()
def add_vital():
    data = request.get_json()
    user_id = get_jwt_identity()
    vital = {
        "userId": user_id,
        "bloodPressure": data.get("bloodPressure"),
        "bloodSugar": data.get("bloodSugar"),
        "heartRate": data.get("heartRate")
    }
    current_app.mongo.db.vitals.insert_one(vital)
    return jsonify({"message": "✅ Vital added"})
