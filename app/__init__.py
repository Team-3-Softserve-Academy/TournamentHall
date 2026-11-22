from flask import Flask
from flask_jwt_extended import JWTManager
from werkzeug.middleware.proxy_fix import ProxyFix
from app.config import Config
from app.blueprints.auth import auth_bp
from app.blueprints.knight_key import knight_key_bp

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(auth_bp)
    app.register_blueprint(knight_key_bp)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

    jwt.init_app(app)

    @app.route('/health')
    def health():
        return {'status': 'ok'}, 200

    return app