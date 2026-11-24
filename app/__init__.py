from flask import Flask, render_template, jsonify, redirect, url_for
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt, unset_jwt_cookies
from werkzeug.middleware.proxy_fix import ProxyFix
from app.config import Config
from app.blueprints.auth import auth_bp
from app.blueprints.knight_key import knight_key_bp
from app.blueprints.books import books_bp
from app.utils.answer_type import wants_json

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt.init_app(app)

    def _auth_failed(message):
        if wants_json():
            response = jsonify({"error": message})
            unset_jwt_cookies(response)
            return response, 401
        response = redirect(url_for('auth.login'))
        unset_jwt_cookies(response)
        return response

    @jwt.unauthorized_loader
    def handle_missing_token(reason):
        return _auth_failed(reason)

    @jwt.expired_token_loader
    def handle_expired_token(jwt_header, jwt_payload):
        return _auth_failed("Token has expired")

    @jwt.invalid_token_loader
    def handle_invalid_token(reason):
        return _auth_failed(reason)

    app.register_blueprint(auth_bp)
    app.register_blueprint(knight_key_bp)
    app.register_blueprint(books_bp)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

    @app.context_processor
    def inject_current_user():
        try:
            verify_jwt_in_request(optional=True)
            claims = get_jwt()
        except Exception:
            claims = {}

        if not claims:
            return {"current_user": None}

        return {"current_user": {
            "id": claims.get("profile_id"),
            "login": claims.get("login"),
            "role": claims.get("role"),
            }
        }

    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/health')
    def health():
        return {'status': 'ok'}, 200

    return app