from __future__ import annotations
from flask import Flask
from .config import Config
from .routes.health import health_bp
from .routes.insights import insights_bp
from .routes.predictions import predictions_bp
from .routes.ui import ui_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(insights_bp)
    app.register_blueprint(predictions_bp)
    app.register_blueprint(ui_bp)

    @app.route('/')
    def index():
        return {'message': 'AI-Powered Data Insight API', 'endpoints': ['/health', '/upload', '/predict', '/ui']}

    return app


if __name__ == '__main__':
    app = create_app()
    # Run without debug auto-reload for stability in container automation
    app.run(host='0.0.0.0', port=8000, debug=False)
