from app import db
from flask_login import UserMixin

class Localidade(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    endereco = db.Column(db.String(120), nullable=False)
    conteudo_id = db.Column(db.Integer, db.ForeignKey('conteudo.id'), nullable=False)
    visitas = db.relationship('Visita', back_populates='localidade')