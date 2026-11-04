from app import db
from flask_login import UserMixin

class Conteudo(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True, nullable=False)
    body = db.Column(db.Text)
    slug = db.Column(db.String(255), unique = True, nullable=False)