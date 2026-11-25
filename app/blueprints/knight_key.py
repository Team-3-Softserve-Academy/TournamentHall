from flask import Blueprint, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt
from app.services.knight_key_service import (
    get_spy_key_status,
    generate_spy_key,
    spy_on_knight,
)
from app.utils.answer_type import wants_json
from app.utils.spy_access import grant_spy_access

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

def _back_to_book(message, category):
    flash(message, category)
    return redirect(url_for("books.book_of_knights"))

def _only_knights():
    if wants_json():
        return jsonify({"error": "Only knight can access spy keys"}), 403
    return _back_to_book("Only knight can access spy keys", "error")


@knight_key_bp.route("/knight/key", methods=["GET", "POST"])
@jwt_required()
def knight_key():
    knight_id = _get_current_knight_id()
    if knight_id is None:
        return _only_knights()

    if request.method == "GET":
        data, err = get_spy_key_status(knight_id=knight_id)
        if err is not None:
            return jsonify({"error": err}), 400
        return jsonify(data), 200

    data, err = generate_spy_key(knight_id=knight_id)

    if wants_json():
        if err is not None:
            return jsonify({"error": err}), 400
        return jsonify({"message": "Spy key generated", "data": data}), 201

    if err is not None:
        return _back_to_book(err, "error")
    return _back_to_book(f"Your gossip password for today: {data['key']}", "success")


@knight_key_bp.route("/knight/<int:target_knight_id>/spy", methods=["POST"])
@jwt_required()
def spy_knight(target_knight_id):
    knight_id = _get_current_knight_id()
    if knight_id is None:
        return _only_knights()

    provided_key = _get_request_data().get("key")
    data, err = spy_on_knight(knight_id, target_knight_id, provided_key)

    if err is None:
        grant_spy_access(knight_id, target_knight_id)

    if wants_json():
        if err is not None:
            return jsonify({"error": err}), 400
        return jsonify({"message": "Knight stats unlocked", "data": data}), 200

    if err is not None:
        return _back_to_book(err, "error")
    return _back_to_book(f"{data['full_name']}'s stats are visible to you until the end of the day", "success")