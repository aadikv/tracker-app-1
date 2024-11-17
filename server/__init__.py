from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
    app.config.from_object(Config)

    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)

    from scheduler import init_scheduler
    init_scheduler(app)

    with app.app_context():
        from . import models
        db.create_all()

        from .views import server_bp
        app.register_blueprint(server_bp)

    return app