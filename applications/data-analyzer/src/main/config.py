import os

class Config:
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'analyzer_database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+db_path