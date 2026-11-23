from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import jwt_required, get_jwt
from app.services.book_service import get_all_lords, get_all_knights

books_bp = Blueprint('books', __name__)

#TEMPORARY ADAPTER. REMOVE AFTER FIXING CONSISTENCY BETWEEN FRONT AND BD

def _adapt_photo(url):
    return "" if url == "default_photo_url" else url


def _adapt_lord_for_template(lord: dict):
    return {
        "id": lord["id"],
        "name": lord["full_name"],
        "house": lord["home"],
        "role": "Lord",
        "image_url": _adapt_photo(lord["photo_url"]),
    }


def _adapt_knight_for_template(knight: dict):
    return {
        "id": knight["id"],
        "name": knight["full_name"],
        "house": knight["home"],
        "role": "Knight",
        "image_url": _adapt_photo(knight["photo_url"]),
        "can_view_stats": knight["stats_visible"],
        "strength": knight["strength"],
        "dexterity": knight["speed"],
        "constitution": knight["protection"],
    }

@books_bp.route('/book-of-lords', methods=['GET'])
@jwt_required()
def book_of_lords():
    lords, err = get_all_lords()
    if err is not None:
        return jsonify({"error": err}), 500

    if request.args.get("format") == "json":
        return jsonify({"lords": lords}), 200

    entries = [_adapt_lord_for_template(lord) for lord in lords]
    return render_template("book.html", entries=entries, role="Lord")

@books_bp.route('/book-of-knights', methods=['GET'])
@jwt_required()
def book_of_knights():
    claims = get_jwt()
    knights, err = get_all_knights(
        current_role=claims.get('role'),
        current_profile_id=claims.get('profile_id'),
    )
    if err is not None:
        return jsonify({"error": err}), 500

    if request.args.get("format") == "json":
        return jsonify({"knights": knights}), 200

    entries = [_adapt_knight_for_template(knight) for knight in knights]
    return render_template("book.html", entries=entries, role="Knight")
