import secrets
from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.utils.db_session import session_scope
from app.utils.validators import has_forbidden_symbols, validate_registration_form
from repositories.common_folk_repository import CommonFolkRepository
from repositories.knight_repository import KnightRepository
from repositories.lord_repository import LordRepository
from repositories.user_repository import UserRepository

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["GET"])
@jwt_required()
def index():
    user_id = int(get_jwt_identity())
    with session_scope() as session:
        user_repo = UserRepository(session)
        user = user_repo.get_by_id(user_id)
        if not user:
            resp = redirect(url_for("auth.login"))
            unset_jwt_cookies(resp)
            return resp
        return render_template("base.html", current_user=user)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", form_data={})

    form_data = {
        "login": request.form.get("login", "").strip(),
        "password": request.form.get("password", ""),
        "in_game_name": request.form.get("in_game_name", "").strip(),
        "role": request.form.get("role", "").strip().lower(),
        "house": request.form.get("house", "").strip(),
        "image_url": request.form.get("image_url", "").strip(),
        "is_white_knight": request.form.get("is_white_knight") == "on",
    }

    errors = validate_registration_form(form_data)
    if errors:
        for err in errors:
            flash(err, "error")
        return render_template("register.html", form_data=form_data), 400

    with session_scope() as session:
        user_repo = UserRepository(session)


        if user_repo.get_by_login(form_data["login"]):
            flash("Користувач із таким логіном уже існує.", "error")
            return render_template("register.html", form_data=form_data), 400

        role = form_data["role"]
        lord_id = None
        knight_id = None
        commonfolk_id = None

        if role == "lord":
            lord_repo = LordRepository(session)
            lord = lord_repo.create_lord(
                name=form_data["in_game_name"],
                image_url=form_data["image_url"],
                house=form_data["house"],
            )
            lord_id = lord.id

        elif role == "knight":
            knight_repo = KnightRepository(session)
            daily_gossip_key = secrets.token_hex(4)
            knight = knight_repo.create_knight(
                name=form_data["in_game_name"],
                image_url=form_data["image_url"],
                strength=10,
                speed=10,
                protection=10,
                house=form_data["house"],
                key=daily_gossip_key,
                key_last_used=datetime.utcnow(),
            )
            knight_id = knight.id

        else:
            folk_repo = CommonFolkRepository(session)
            folk = folk_repo.create_commonfolk(name=form_data["in_game_name"])
            commonfolk_id = folk.id

        password_hash = generate_password_hash(form_data["password"])
        is_white = form_data["is_white_knight"] if role == "knight" else False

        new_user = user_repo.create_user(
            login=form_data["login"],
            password_hash=password_hash,
            role=role,
            is_white_knight=is_white,
            lord_id=lord_id,
            knight_id=knight_id,
            commonfolk_id=commonfolk_id,
        )

        user_repo.record_ip(new_user.id, request.remote_addr)

        access_token = create_access_token(identity=str(new_user.id))
        response = redirect(url_for("auth.index"))
        set_access_cookies(response, access_token)
        flash("Реєстрація успішна! Ласкаво просимо до Залу Турнірів.", "success")
        return response


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", login_value="")

    login_input = request.form.get("login", "").strip()
    password_input = request.form.get("password", "")

    if not login_input or not password_input:
        flash("Введіть логін та пароль.", "error")
        return render_template("login.html", login_value=login_input), 400

    if has_forbidden_symbols(login_input):
        flash("Логін містить заборонені символи: ; ' [ ] . , ( )", "error")
        return render_template("login.html", login_value=login_input), 400

    with session_scope() as session:
        user_repo = UserRepository(session)
        user = user_repo.get_by_login(login_input)

        if not user or not check_password_hash(user.password_hash, password_input):
            flash("Невірний логін або пароль.", "error")
            return render_template("login.html", login_value=login_input), 401

        user_repo.record_ip(user.id, request.remote_addr)

        access_token = create_access_token(identity=str(user.id))
        response = redirect(url_for("auth.index"))
        set_access_cookies(response, access_token)
        return response


@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    response = redirect(url_for("auth.login"))
    unset_jwt_cookies(response)
    flash("Ви вийшли з облікового запису.", "info")
    return response