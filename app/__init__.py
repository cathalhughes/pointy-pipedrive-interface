from flask import Flask
from app.config import Config





def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.closest_organisations import bp as closest_organisations_bp
    app.register_blueprint(closest_organisations_bp)

    return app


