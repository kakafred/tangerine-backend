from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from app.extensions import db
from app.extensions import login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    CORS(app)
    login_manager.init_app(app)

    from app.authentication import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp)

    from app.categories import bp as categories_bp
    app.register_blueprint(categories_bp)

    from app.tags import bp as tags_bp
    app.register_blueprint(tags_bp)

    from app.comments import bp as comments_bp
    app.register_blueprint(comments_bp)

    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({"error": "Oops, bad request..."}), 400

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Oops, resource not found..."}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": "Oops, internal server error..."}), 500

    return app
