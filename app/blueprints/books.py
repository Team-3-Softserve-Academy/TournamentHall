from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.services.book_service import get_all_lords, get_all_knights

books_bp = Blueprint('books', __name__)

@books_bp.route('/book-of-lords', methods=['GET'])
@jwt_required()
def book_of_lords():
    lords, err = get_all_lords()
    if err is not None:
        return jsonify({"error": err}), 500
    return jsonify({"lords": lords}), 200

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
    return jsonify({"knights": knights}), 200