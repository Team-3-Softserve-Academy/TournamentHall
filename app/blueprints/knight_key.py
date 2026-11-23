from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from app.services.knight_key_service import (
    get_spy_key_status,
    generate_spy_key,
    spy_on_knight,
)

knight_key_bp = Blueprint("knight_key", __name__)

def _get_current_knight_id():
    claims = get_jwt()
    if claims.get("role") != "Knight":
        return None
    profile_id = claims.get("profile_id")
    return int(profile_id) if profile_id is not None else None

def _get_request_data():
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else request.form.to_dict()


@knight_key_bp.route("/knight/key", methods=["GET", "POST"])
@jwt_required()
def knight_key():
    if _get_current_knight_id() is None:
        return jsonify({"error": "Only knight can access spy keys"}), 403

    if request.method == "GET":
        data, err = get_spy_key_status(knight_id=_get_current_knight_id())
        if err is not None:
            return jsonify({"error": err}), 400
        return jsonify(data), 200

    if request.method == "POST":
        data, err = generate_spy_key(knight_id=_get_current_knight_id())
        if err is not None:
            return jsonify({"error": err}), 400
        return jsonify({"message": "Spy key generated", "data": data}), 201


@knight_key_bp.route("/knight/<int:target_knight_id>/spy", methods=["POST"])
@jwt_required()
def spy_knight(target_knight_id):
    if _get_current_knight_id() is None:
        return jsonify({"error": "Only knight can access spy keys"}), 403

    provided_key = _get_request_data().get("key")

    data, err = spy_on_knight(_get_current_knight_id(), target_knight_id, provided_key)

    if err is not None:
        return jsonify({"error": err}), 400
    return jsonify({"message": "Knight stats unlocked", "data": data}), 200