from flask_sqlalchemy import SQLAlchemy

class Database:
    def __init__(self, app):
        self.db = SQLAlchemy(app)