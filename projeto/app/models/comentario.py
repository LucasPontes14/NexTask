from app import db
from flask_login import UserMixin

class Comentario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    conteudo_id = db.Column(db.Integer, db.ForeignKey("conteudo.id"), nullable=False)
    body = db.Column(db.String(2000), nullable = False)
    slug = db.Column(db.String(255), unique = True, nullable=False)
    data_hora = db.Column(db.DateTime)
    usuario = db.relationship("Usuario")
    conteudo = db.relationship("Conteudo", back_populates="comentarios")