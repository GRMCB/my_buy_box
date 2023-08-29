from flask import Flask
from config import Config
def create_app(config_obj=Config):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    from database.models import db
    db.init_app(app)

    return app