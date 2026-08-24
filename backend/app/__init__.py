from flask import Flask


def create_app():
    app = Flask(__name__)

    from app.timeline_suggestions.routes import timeline_bp
    app.register_blueprint(timeline_bp)

    return app