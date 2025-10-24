from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

appointment_bp = Blueprint("appointment_bp", __name__)

@appointment_bp.route("/", methods=["GET"])
@jwt_required()
def get_appointments():
    user_id = get_jwt_identity()
    appts = list(current_app.mongo.db.appointments.find({"userId": user_id}))
    for a in appts:
        a["_id"] = str(a["_id"])
    return jsonify(appts)

@appointment_bp.route("/", methods=["POST"])
@jwt_required()
def add_appointment():
    data = request.get_json()
    user_id = get_jwt_identity()
    appt = {"userId": user_id, "doctor": data["doctor"], "date": data["date"]}
    current_app.mongo.db.appointments.insert_one(appt)
    return jsonify({"message": "✅ Appointment added"})
