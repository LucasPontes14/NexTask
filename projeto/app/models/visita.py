from app import db
from flask_login import UserMixin

class Visita(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    localidade_id = db.Column(db.Integer, db.ForeignKey('localidade.id'), nullable=False)
    data_hora = db.Column(db.DateTime)
    usuario = db.relationship('Usuario', back_populates='visitas')
    localidade = db.relationship('Localidade', back_populates='visitas')