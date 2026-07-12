from typing import Optional
import mysql.connector
from src.dominio.lista import Lista

class ListRepository:
    def __init__(self, conexao: mysql.connector.MySQLConnection) -> None:
        self.conexao = conexao
        self._criar_tabela()
    
    def _criar_tabela(self) -> None:
        sql = """
        CREATE TABLE IF NOT EXISTS lista(
            id_lista INT NOT NULL AUTO_INCREMENT,
            id_usuario INT NOT NULL,
            nome VARCHAR(100) NOT NULL,
            criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id_lista),
            FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
        )
        """
        cursor = self.conexao.cursor()
        cursor.execute(sql)
        self.conexao.commit()
        cursor.close()

    def adicionar(self, lista: Lista) -> int:
        cursor = self.conexao.cursor()
        cursor.execute(
            "INSERT INTO lista (id_usuario, nome) VALUES (%s, %s)",
            (lista.id_usuario, lista.nome)
        )
        self.conexao.commit()
        novo_id = int(cursor.lastrowid)
        cursor.close()
        return novo_id
    
    def listar_todas(self) -> list[Lista]:
        cursor = self.conexao.cursor(dictionary=True)
        cursor.execute("SELECT id_lista, id_usuario, nome, criado_em FROM lista ORDER BY id_lista")
        linhas = cursor.fetchall()
        cursor.close()
        return [
            Lista(
                id_lista=l["id_lista"],
                id_usuario=l["id_usuario"],
                nome=l["nome"],
                criado_em=l["criado_em"]
            )
            for l in linhas
        ]
    
    def listar_por_usuario(self, id_usuario: int) -> list[Lista]:
        cursor = self.conexao.cursor(dictionary=True)
        cursor.execute(
            "SELECT id_lista, id_usuario, nome, criado_em FROM lista WHERE id_usuario = %s ORDER BY id_lista",  
            (id_usuario,),
        )
        linhas = cursor.fetchall()
        cursor.close()
        return [
            Lista(
                id_lista=l["id_lista"],
                id_usuario=l["id_usuario"],
                nome=l["nome"],
                criado_em=l["criado_em"],
            )
            for l in linhas
        ]
    
    def buscar_por_id(self, id_lista: int) -> Optional[Lista]:
        cursor = self.conexao.cursor(dictionary=True)
        cursor.execute(
            "SELECT id_lista, id_usuario, nome, criado_em FROM lista WHERE id_lista = %s",
            (id_lista,),  
        )
        linha = cursor.fetchone()  
        cursor.close()
        if linha is None:
            return None
        return Lista(
            id_lista=linha["id_lista"],
            id_usuario=linha["id_usuario"],
            nome=linha["nome"],
            criado_em=linha["criado_em"],
        )
    
    def atualizar(self, lista: Lista) -> bool:
        cursor = self.conexao.cursor()
        cursor.execute(
            "UPDATE lista SET nome = %s WHERE id_lista = %s",
            (lista.nome, lista.id_lista),
        )
        self.conexao.commit()
        afetados = cursor.rowcount > 0 
        cursor.close()
        return afetados
    
    def remover(self, id_lista: int) -> bool:
        cursor = self.conexao.cursor()
        cursor.execute("DELETE FROM lista WHERE id_lista = %s", (id_lista,))  
        self.conexao.commit()
        afetados = cursor.rowcount > 0
        cursor.close()
        return afetados