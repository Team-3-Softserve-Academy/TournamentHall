from flask import Blueprint, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt
from app.services.knight_key_service import (
    generate_spy_key,
    spy_on_knight,
)
from app.utils.spy_access import grant_spy_access

knight_key_bp = Blueprint("knight_key", __name__)

def _get_current_knight_id():
    claims = get_jwt()
    if claims.get("role") != "Knight":
        return None
    profile_id = claims.get("profile_id")
    return int(profile_id) if profile_id is not None else None

def _back_to_book(message, category):
    flash(message, category)
    return redirect(url_for("books.book_of_knights"))

def _only_knights():
    return _back_to_book("Only knight can access spy keys", "error")


@knight_key_bp.route("/knight/key", methods=["POST"])
@jwt_required()
def knight_key():
    knight_id = _get_current_knight_id()
    if knight_id is None:
        return _only_knights()

    data, err = generate_spy_key(knight_id=knight_id)

    if err is not None:
        return _back_to_book(err, "error")
    return _back_to_book(f"Your gossip password for today: {data['key']}", "success")


@knight_key_bp.route("/knight/<int:target_knight_id>/spy", methods=["POST"])
@jwt_required()
def spy_knight(target_knight_id):
    knight_id = _get_current_knight_id()
    if knight_id is None:
        return _only_knights()

    provided_key = request.form.get("key")
    data, err = spy_on_knight(knight_id, target_knight_id, provided_key)

    if err is not None:
        return _back_to_book(err, "error")

    grant_spy_access(knight_id, target_knight_id)
    return _back_to_book(f"{data['full_name']}'s stats are visible to you until the end of the day", "success")