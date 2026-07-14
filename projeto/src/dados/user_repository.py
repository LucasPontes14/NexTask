from typing import Optional
import mysql.connector
from src.dominio.usuario import Usuario


class UsuarioRepository:
    def __init__(self, conexao: mysql.connector.MySQLConnection) -> None:
        self.conexao = conexao

    def adicionar(self, usuario: Usuario) -> int:
        cursor = self.conexao.cursor()
        sql = """
            INSERT INTO usuario (nome, email, senha)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (usuario.nome, usuario.email, usuario.senha))
        self.conexao.commit()
        novo_id = cursor.lastrowid
        cursor.close()
        return novo_id

    def buscar_por_id(self, id_usuario: int) -> Optional[Usuario]:
        cursor = self.conexao.cursor()
        cursor.execute("SELECT id_usuario, nome, email, senha FROM usuario WHERE id_usuario = %s", (id_usuario,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None
        return Usuario(id_usuario=row[0], nome=row[1], email=row[2], senha=row[3], criado_em=None)

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        cursor = self.conexao.cursor()
        cursor.execute("SELECT id_usuario, nome, email, senha FROM usuario WHERE email = %s", (email,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None
        return Usuario(id_usuario=row[0], nome=row[1], email=row[2], senha=row[3], criado_em=None)

    def listar_todos(self) -> list[Usuario]:
        cursor = self.conexao.cursor()
        cursor.execute("SELECT id_usuario, nome, email, senha FROM usuario")
        rows = cursor.fetchall()
        cursor.close()
        return [Usuario(id_usuario=row[0], nome=row[1], email=row[2], senha=row[3], criado_em=None) for row in rows]

    def atualizar(self, usuario: Usuario) -> bool:
        cursor = self.conexao.cursor()
        sql = """
            UPDATE usuario
            SET nome = %s, email = %s, senha = %s
            WHERE id_usuario = %s
        """
        cursor.execute(sql, (usuario.nome, usuario.email, usuario.senha, usuario.id_usuario))
        self.conexao.commit()
        atualizado = cursor.rowcount > 0
        cursor.close()
        return atualizado

    def remover(self, id_usuario: int) -> bool:
        cursor = self.conexao.cursor()
        cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))
        self.conexao.commit()
        removido = cursor.rowcount > 0
        cursor.close()
        return removido