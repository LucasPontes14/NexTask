from typing import Optional
from dados.tarefa_repository import TaskRepository
from dominio.tarefa import Tarefa

class TarefaService:
    def __init__(self, repositorio: TaskRepository) -> None:
        self.repositorio = repositorio
    
    def cadastrar_tarefa(self, titulo: str) -> Tarefa:
     titulo_limpo = titulo.strip()
     if not titulo_limpo:
        raise ValueError("O titulo de uma tarefa não pode ficar vazio")
     tarefa = Tarefa(id=None, titulo = titulo_limpo)
     novo_id = self.repositorio.adicionar(tarefa)
     tarefa.id_tarefa = novo_id
     return tarefa 

    # def listar_tarefas(self, id_lista) -> list[Tarefa]:
    #     tarefa.id_lista = id_lista
    #     return self.repositorio.listar_por_lista(id_lista)

    # def buscar_tarefa_por_id(self, id_lista: int)

    def atualizar_tarefa(self, id_tarefa: int, titulo: str, descricao: str, prioridade: str, status: str, data_venc: str, hora_venc: str, criado_em: str) -> bool:
        if id_tarefa <= 0:
            raise ValueError("O ID da tarefa deve ser um número inteiro positivo.")
        titulo_limpo = titulo.strip()
        if not titulo_limpo:
           raise ValueError("O titulo da tarefa não pode ficar vazio")
        
        if len(titulo_limpo) > 200:
            raise ValueError("O título de uma tarefa não pode ultrapassar 200 caracteres.")
        
        tarefa = self.repositorio.buscar_por_id(id_tarefa)

        if tarefa is None:
           return False
        
        tarefa.titulo = titulo_limpo
        return self.repositorio.atualizar(tarefa)


    def excluir_tarefa(self, id_tarefa: int):
       tarefa = self.repositorio.buscar_por_id(id_tarefa)

       if tarefa is None:
          return False
       
       return self.repositorio.remover(id_tarefa)