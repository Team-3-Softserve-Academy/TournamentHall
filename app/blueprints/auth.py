from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from app.services.auth_service import register_user, authenticate_user

auth_bp = Blueprint("auth", __name__)

def _get_request_data():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form.to_dict()

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        data = _get_request_data()
        user_data, err = register_user(data)
        if err:
            return jsonify({"error": err}), 400

        access_token = create_access_token(
            identity=str(user_data["user_id"]),
            additional_claims={
                "role": user_data["role"],
                "login": user_data["login"],
                "profile_id": user_data["profile_id"],
            }
        )

        response = jsonify({"message": "Registered successfully", "user": user_data})
        set_access_cookies(response, access_token)
        return response, 201


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        data = _get_request_data()
        user_data, err = authenticate_user(data.get("login"), data.get("password"))

        if err:
            return jsonify({"error": err}), 401

        access_token = create_access_token(
            identity=str(user_data["user_id"]),
            additional_claims={
                "role": user_data["role"],
                "login": user_data["login"],
                "profile_id": user_data["profile_id"],
            }
        )

        response = jsonify({"message": "Logged in successfully", "user": user_data})
        set_access_cookies(response, access_token)
        return response, 200


@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    response = jsonify({"message": "Logged out"})
    unset_jwt_cookies(response)
    return response, 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    return jsonify({
        "user_id": get_jwt_identity(),
        "login": get_jwt().get("login"),
        "role": get_jwt().get("role"),
        "profile_id": get_jwt().get("profile_id"),
    }), 200