from flask import Flask, jsonify
from .config import Config
from .extensions import cors
from .routes.salary import bp as salary_bp
from .ui.views import bp as ui_bp   
from .routes.agent import bp as agent_bp   # <— add

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(Config)

    cors.init_app(app)

    # API
    app.register_blueprint(salary_bp, url_prefix="/api/salary")
    app.register_blueprint(agent_bp,  url_prefix="/api/agent")   # <— add


    # UI
    app.register_blueprint(ui_bp, url_prefix="")

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    return app
