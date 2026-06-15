from flask import Flask
from app.messaging import BusInterface


def create_app(bus: BusInterface):

    app = Flask(__name__)

    from .api.routes import bp as health_bp
    app.register_blueprint(health_bp)

    print("App created successfully")

    return app
