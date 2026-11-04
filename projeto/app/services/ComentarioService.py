from app import db
from app.models import Comentario, Conteudo, Usuario
import sqlalchemy as sa

class ComentarioService():
    @staticmethod
    def criar_comentario(form):
        try:
            comentario = Comentario()
            form.populate_obj(comentario)
            db.session.add(comentario)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(e)
            return False
        
    @staticmethod
    def listar_comentarios():
        query = sa.select(Comentario)
        return db.session.scalars(query).all()
        
    @staticmethod
    def editar_comentario(comentario, form, usuario):
        if comentario.usuario_id != usuario.id:
            return False
        try:
            form.populate_obj(comentario)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(e)
            return False
    
    @staticmethod
    def excluir_comentario(comentario):
        try:
            db.session.delete(comentario)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(e)
            return False