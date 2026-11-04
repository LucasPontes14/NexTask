import os
from urllib.parse import quote_plus

class Config:
    SECRET_KEY = 'chave-secreta'
    DB_PASSWORD = os.getenv("DB_PASSWORD", "labinfo") 
    DB_USERNAME = os.getenv("DB_USERNAME", "root")
    DB_NAME = "db_portal_cm"
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USERNAME}:{quote_plus(DB_PASSWORD)}@localhost:3306/{DB_NAME}"