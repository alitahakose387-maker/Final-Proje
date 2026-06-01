from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Bu sayfayı görmek için giriş yapmalısınız."
login_manager.login_message_category = "warning"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Extension'ları başlat
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Modelleri import et (migrate tarafından algılanması için)
    from app import models  # noqa: F401

    # Blueprint'leri kaydet
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.main import main_bp
    app.register_blueprint(main_bp)

    return app
