from typing import Optional
from src.dados.tarefa_repository import TaskRepository
from src.dominio.tarefa import Tarefa

class TarefaService:
    def __init__(self, repositorio: TaskRepository) -> None:
        self.repositorio = repositorio

    def cadastrar_tarefa(
        self,
        id_lista: int,
        titulo: str,
        descricao: str = "",
        prioridade: str = "media",
        status: str = "pendente",
        data_inicio=None,
        data_venc=None,
        hora_venc=None,
    ) -> Tarefa:
        if id_lista <= 0:
            raise ValueError("O ID da lista deve ser um número inteiro positivo.")

        titulo_limpo = titulo.strip()
        if not titulo_limpo:
            raise ValueError("O título de uma tarefa não pode ficar vazio.")
        if len(titulo_limpo) > 200:
            raise ValueError("O título de uma tarefa não pode ultrapassar 200 caracteres.")

        if data_inicio and data_venc and data_inicio > data_venc:
            raise ValueError("A data de início não pode ser depois do prazo (vencimento).")

        tarefa = Tarefa(
            id_tarefa=None,
            id_lista=id_lista,
            titulo=titulo_limpo,
            descricao=descricao,
            prioridade=prioridade,
            status=status,
            data_inicio=data_inicio,
            data_venc=data_venc,
            hora_venc=hora_venc,
            criado_em=None,
        )
        novo_id = self.repositorio.adicionar(tarefa)
        tarefa.id_tarefa = novo_id
        return tarefa

    def listar_tarefas(self, id_lista: int) -> list[Tarefa]:
        if id_lista <= 0:
            raise ValueError("O ID da lista deve ser um número inteiro positivo.")
        return self.repositorio.listar_por_lista(id_lista)

    def listar_por_usuario(self, id_usuario: int) -> list[Tarefa]:
        """Lista apenas as tarefas cujas listas pertencem a este usuário."""
        if id_usuario <= 0:
            raise ValueError("O ID do usuário deve ser um número inteiro positivo.")
        return self.repositorio.listar_por_usuario(id_usuario)

    def listar_todas(self) -> list[Tarefa]:
        """ATENÇÃO: retorna tarefas de TODOS os usuários, sem filtro.
        Não usar na interface — apenas para uso administrativo/depuração.
        Para exibir tarefas de um usuário, use listar_por_usuario()."""
        return self.repositorio.listar_todas()

    def buscar_tarefa_por_id(self, id_tarefa: int) -> Optional[Tarefa]:
        if id_tarefa <= 0:
            raise ValueError("O ID da tarefa deve ser um número inteiro positivo.")
        return self.repositorio.buscar_por_id(id_tarefa)

    def atualizar_tarefa(
        self,
        id_tarefa: int,
        titulo: str,
        descricao: str = "",
        prioridade: str = "media",
        status: str = "pendente",
        data_inicio=None,
        data_venc=None,
        hora_venc=None,
    ) -> bool:
        if id_tarefa <= 0:
            raise ValueError("O ID da tarefa deve ser um número inteiro positivo.")

        titulo_limpo = titulo.strip()
        if not titulo_limpo:
            raise ValueError("O título da tarefa não pode ficar vazio.")
        if len(titulo_limpo) > 200:
            raise ValueError("O título de uma tarefa não pode ultrapassar 200 caracteres.")

        if data_inicio and data_venc and data_inicio > data_venc:
            raise ValueError("A data de início não pode ser depois do prazo (vencimento).")

        tarefa = self.repositorio.buscar_por_id(id_tarefa)
        if tarefa is None:
            return False

        tarefa.titulo = titulo_limpo
        tarefa.descricao = descricao
        tarefa.prioridade = prioridade
        tarefa.status = status
        tarefa.data_inicio = data_inicio
        tarefa.data_venc = data_venc
        tarefa.hora_venc = hora_venc
        return self.repositorio.atualizar(tarefa)

    def excluir_tarefa(self, id_tarefa: int) -> bool:
        if id_tarefa <= 0:
            raise ValueError("O ID da tarefa deve ser um número inteiro positivo.")

        tarefa = self.repositorio.buscar_por_id(id_tarefa)
        if tarefa is None:
            return False

        return self.repositorio.remover(id_tarefa)