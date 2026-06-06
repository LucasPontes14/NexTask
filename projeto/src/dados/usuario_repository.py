from typing import Optional
import mysql.connector
from dominio.usuario import Usuario

class usuarioRepository:
    def __init__(self, conexao: mysql.connector.MySQLConnection) -> None:
        self.conexao = conexao

    def adicionar(self, usuario: Usuario) -> int:
        cursor = self.conexao.cursor()
        # Cursor é o objeto usado para executar os comandos SQL
        # self.conexao é a conexao é a conexao com o banco de dados
        cursor.execute("INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)", (usuario.nome, usuario.email, usuario.senha))
        self.conexao.commit() # Confirma a transação
        novo_id = int(cursor.lastrowid)
        cursor.close()
        return novo_id
    
    def listar_todas(self) -> list[Usuario]:
        cursor = self.conexao.cursor(dictionary=True)
        cursor.execute("SELECT id_usuario, nome, email, senha, criado_em FROM usuario ORDER BY id_usuario")
        linhas = cursor.fetchall()
        cursor.close()
        return [Usuario(id_usuario=linha["id_usuario"], nome=linha["nome"], email = linha["email"], senha=linha["senha"], criado_em=linha["criado_em"]) for linha in linhas]
    
    def buscar_por_id(self, id_usuario: int) -> Optional[Usuario]:
        cursor = self.conexao.cursor(dictionary=True)
        cursor.execute("SELECT id_usuario, nome, email, senha, criado_em FROM usuario WHERE id = %s", (id_usuario,),)
        linha = cursor.fetchone()
        cursor.close()
        if linha is None:
            return None
        return Usuario(id_usuario=linha["id_usuario"], nome=linha["nome"], email=linha["email"], senha=linha["senha"], criado_em=linha["criado_em"])
    
    def atualizar(self, usuario: Usuario) -> bool:
        cursor = self.conexao.cursor()
        cursor.execute("UPDATE usuario SET nome = %s, email = %s, senha = %s WHERE id_usuario = %s", (usuario.nome, usuario.email, usuario.senha, usuario.id_usuario),)
        self.conexao.commit()
        afetados = cursor.rowcount > 0
        cursor.close()
        return afetados
    
    def remover(self, id_usuario: int) -> bool:
        cursor = self.conexao.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id_usuario,),)
        self.conexao.commit()
        afetados = cursor.rowcount > 0
        cursor.close()
        return afetados