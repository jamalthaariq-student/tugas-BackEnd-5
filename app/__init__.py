from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Mendaftarkan routes (Blueprint)
    from app.routes.v1.product_routes import product_bp
    app.register_blueprint(product_bp)
    from app.routes.v1.users_routes import user_bp_v1
    app.register_blueprint(user_bp_v1)

    return app