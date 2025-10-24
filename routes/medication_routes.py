from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

medication_bp = Blueprint("medication_bp", __name__)

@medication_bp.route("/", methods=["GET"])
@jwt_required()
def get_medications():
    user_id = get_jwt_identity()
    meds = list(current_app.mongo.db.medications.find({"userId": user_id}))
    for m in meds:
        m["_id"] = str(m["_id"])
    return jsonify(meds)

@medication_bp.route("/", methods=["POST"])
@jwt_required()
def add_medication():
    data = request.get_json()
    user_id = get_jwt_identity()
    med = {"userId": user_id, "name": data["name"], "time": data["time"]}
    current_app.mongo.db.medications.insert_one(med)
    return jsonify({"message": "✅ Medication added"})
