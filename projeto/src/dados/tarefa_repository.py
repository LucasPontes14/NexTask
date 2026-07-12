from typing import Optional
import mysql.connector
from src.dominio.tarefa import Tarefa

class TaskRepository:
    def __init__(self, conexao: mysql.connector.MySQLConnection) -> None:
        self.conexao = conexao
        self._criar_tabela()

    def _criar_tabela(self) -> None:
        sql = """
        CREATE TABLE IF NOT EXISTS tarefa(
            id_tarefa INT NOT NULL AUTO_INCREMENT,
            id_lista INT NOT NULL,
            titulo VARCHAR(200) NOT NULL,
            descricao TEXT,
            prioridade ENUM('baixa', 'media', 'alta') NOT NULL DEFAULT 'media',
            status ENUM('pendente', 'em_andamento', 'concluida') NOT NULL DEFAULT 'pendente',
            data_inicio DATE,
            data_venc DATE,
            hora_venc TIME,
            criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id_tarefa),
            FOREIGN KEY (id_lista) REFERENCES lista(id_lista) ON DELETE CASCADE
        )
        """
        cursor = self.conexao.cursor()
        cursor.execute(sql)
        self.conexao.commit()
        cursor.close()

    def adicionar(self, tarefa: Tarefa) -> int:
        cursor = self.conexao.cursor()
        cursor.execute(
            """
            INSERT INTO tarefa (id_lista, titulo, descricao, prioridade, status, data_inicio, data_venc, hora_venc)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                tarefa.id_lista,
                tarefa.titulo,
                tarefa.descricao,
                tarefa.prioridade,
                tarefa.status,
                tarefa.data_inicio,
                tarefa.data_venc,
                tarefa.hora_venc,
            )
        )
        self.conexao.commit()
        novo_id = int(cursor.lastrowid)
        cursor.close()
        return novo_id

    def listar_todas(self) -> list[Tarefa]:
        cursor = self.conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tarefa ORDER BY id_tarefa")
        linhas = cursor.fetchall()
        cursor.close()
        return [self._linha_para_tarefa(l) for l in linhas]

    def listar_por_lista(self, id_lista: int) -> list[Tarefa]:
        cursor = self.conexao.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM tarefa WHERE id_lista = %s ORDER BY id_tarefa",
            (id_lista,),
        )
        linhas = cursor.fetchall()
        cursor.close()
        return [self._linha_para_tarefa(l) for l in linhas]

    def buscar_por_id(self, id_tarefa: int) -> Optional[Tarefa]:
        cursor = self.conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tarefa WHERE id_tarefa = %s", (id_tarefa,))
        linha = cursor.fetchone()
        cursor.close()
        if linha is None:
            return None
        return self._linha_para_tarefa(linha)

    def atualizar(self, tarefa: Tarefa) -> bool:
        cursor = self.conexao.cursor()
        cursor.execute(
            """
            UPDATE tarefa
            SET id_lista = %s, titulo = %s, descricao = %s,
                prioridade = %s, status = %s, data_inicio = %s,
                data_venc = %s, hora_venc = %s
            WHERE id_tarefa = %s
            """,
            (
                tarefa.id_lista,
                tarefa.titulo,
                tarefa.descricao,
                tarefa.prioridade,
                tarefa.status,
                tarefa.data_inicio,
                tarefa.data_venc,
                tarefa.hora_venc,
                tarefa.id_tarefa,
            ),
        )
        self.conexao.commit()
        afetados = cursor.rowcount > 0
        cursor.close()
        return afetados

    def remover(self, id_tarefa: int) -> bool:
        cursor = self.conexao.cursor()
        cursor.execute("DELETE FROM tarefa WHERE id_tarefa = %s", (id_tarefa,))
        self.conexao.commit()
        afetados = cursor.rowcount > 0
        cursor.close()
        return afetados

    @staticmethod
    def _linha_para_tarefa(linha: dict) -> Tarefa:
        return Tarefa(
            id_tarefa=linha["id_tarefa"],
            id_lista=linha["id_lista"],
            titulo=linha["titulo"],
            descricao=linha["descricao"],
            prioridade=linha["prioridade"],
            status=linha["status"],
            data_inicio=linha["data_inicio"],
            data_venc=linha["data_venc"],
            hora_venc=linha["hora_venc"],
            criado_em=linha["criado_em"],
        )