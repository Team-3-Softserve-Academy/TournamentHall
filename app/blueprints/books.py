from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import jwt_required, get_jwt
from app.services.book_service import get_all_lords, get_all_knights
from app.services.knight_key_service import get_spy_key_status
from app.utils.spy_access import get_active_target

books_bp = Blueprint('books', __name__)

@books_bp.route('/book-of-lords', methods=['GET'])
@jwt_required()
def book_of_lords():
    lords, err = get_all_lords()
    if err is not None:
        return jsonify({"error": err}), 500

    if request.args.get("format") == "json":
        return jsonify({"lords": lords}), 200

    return render_template("book.html", entries=lords, role="Lord")

@books_bp.route('/book-of-knights', methods=['GET'])
@jwt_required()
def book_of_knights():
    claims = get_jwt()
    is_knight = claims.get("role") == "Knight" and claims.get("profile_id") is not None
    knight_id = int(claims["profile_id"]) if is_knight else None

    unlocked_id = get_active_target(knight_id) if is_knight else None

    knights, err = get_all_knights(
        current_role=claims.get('role'),
        current_profile_id=claims.get('profile_id'),
        unlocked_id=unlocked_id,
    )
    if err is not None:
        return jsonify({"error": err}), 500

    if request.args.get("format") == "json":
        return jsonify({"knights": knights}), 200

    gossip_used_today = False
    if is_knight:
        status, _ = get_spy_key_status(knight_id)
        gossip_used_today = bool(status) and not status["can_generate"]

    return render_template(
        "book.html",
        entries=knights,
        role="Knight",
        gossip_used_today=gossip_used_today,
    )
