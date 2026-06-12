from flask import Flask


def create_app():

    app = Flask(__name__)

    from app.api.routes import bp as health_bp
    app.register_blueprint(health_bp)

    print("App created successfully")

    return app
