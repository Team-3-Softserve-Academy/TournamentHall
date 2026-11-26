from flask import Blueprint, request, render_template, redirect, url_for, make_response
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    get_jwt_identity,
    verify_jwt_in_request,
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


def _is_logged_in():
    try:
        verify_jwt_in_request(optional=True)
        return get_jwt_identity() is not None
    except Exception:
        return False

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if _is_logged_in():
            return redirect(url_for("index"))
        return render_template(
            "register.html",
            houses=HOUSES,
            errors={},
            form_data={"role": "Knight"})

    data = request.form.to_dict()
    user_data, err = register_user(data)
    if err:
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

    response = make_response(redirect(url_for("index")))
    set_access_cookies(response, access_token)
    return response


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if _is_logged_in():
            return redirect(url_for("index"))
        return render_template("login.html", errors={}, form_data={})

    data = request.form.to_dict()
    user_data, err = authenticate_user(data.get("login"), data.get("password"))

    if err:
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

    response = make_response(redirect(url_for("index")))
    set_access_cookies(response, access_token)
    return response


@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = make_response(redirect(url_for("auth.login")))
    unset_jwt_cookies(response)
    return response