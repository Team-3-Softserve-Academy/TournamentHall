from flask import Blueprint, request, jsonify, render_template, redirect, url_for, make_response
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


HOUSES = [
    {"name": "House Vance"},
    {"name": "House Corbray"},
    {"name": "House Hightower"},
    {"name": "House Tarly"},
    {"name": "House Blackwood"},
]


def _get_request_data():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form.to_dict()


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template(
            "register.html",
            houses=HOUSES,
            errors={},
            form_data={"role": "Knight"})

    data = _get_request_data()
    user_data, err = register_user(data)
    if err:
        if request.is_json:
            return jsonify({"error": err}), 400
        return render_template(
            "register.html",
            houses=HOUSES,
            errors={},
            form_data=data,
            error_banner=err,
        ), 400

    access_token = create_access_token(
        identity=str(user_data["user_id"]),
        additional_claims={
            "role": user_data["role"],
            "login": user_data["login"],
            "profile_id": user_data["profile_id"],
        }
    )

    if request.is_json:
        response = jsonify({"message": "Registered successfully", "user": user_data})
        set_access_cookies(response, access_token)
        return response, 201

    response = make_response(redirect(url_for("index")))
    set_access_cookies(response, access_token)
    return response


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", errors={}, form_data={})

    data = _get_request_data()
    user_data, err = authenticate_user(data.get("login"), data.get("password"))

    if err:
        if request.is_json:
            return jsonify({"error": err}), 401
        return render_template(
            "login.html",
            errors={},
            form_data=data,
            error_banner=err,
        ), 401

    access_token = create_access_token(
        identity=str(user_data["user_id"]),
        additional_claims={
            "role": user_data["role"],
            "login": user_data["login"],
            "profile_id": user_data["profile_id"],
        }
    )

    if request.is_json:
        response = jsonify({"message": "Logged in successfully", "user": user_data})
        set_access_cookies(response, access_token)
        return response, 200

    response = make_response(redirect(url_for("index")))
    set_access_cookies(response, access_token)
    return response


@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    if request.is_json:
        response = jsonify({"message": "Logged out"})
        unset_jwt_cookies(response)
        return response, 200

    response = make_response(redirect(url_for("auth.login")))
    unset_jwt_cookies(response)
    return response


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    return jsonify({
        "user_id": get_jwt_identity(),
        "login": get_jwt().get("login"),
        "role": get_jwt().get("role"),
        "profile_id": get_jwt().get("profile_id"),
    }), 200