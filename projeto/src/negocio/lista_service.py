from typing import Optional

from dados.lista_repository import ListaRepository
from dominio.lista import Lista


class ListaService:
    """Camada de negócio: aplica validações e regras da lista de tarefas."""

    def __init__(self, repositorio: ListaRepository) -> None:
        self.repositorio = repositorio

    def cadastrar_lista(self, id_usuario: int, nome: str) -> Lista:
        if id_usuario <= 0:
            raise ValueError("O ID do usuário deve ser um número inteiro positivo.")

        nome_limpo = nome.strip()
        if not nome_limpo:
            raise ValueError("O nome da lista não pode ficar vazio.")

        if len(nome_limpo) > 100:
            raise ValueError("O nome da lista não pode ultrapassar 100 caracteres.")

        lista = Lista(id=None, id_usuario=id_usuario, nome=nome_limpo)
        novo_id = self.repositorio.adicionar(lista)
        lista.id = novo_id
        return lista

    def listar_por_usuario(self, id_usuario: int) -> list[Lista]:
        if id_usuario <= 0:
            raise ValueError("O ID do usuário deve ser um número inteiro positivo.")
        return self.repositorio.listar_por_usuario(id_usuario)

    def buscar_lista_por_id(self, id_lista: int, id_usuario: int) -> Optional[Lista]:
        if id_lista <= 0:
            raise ValueError("O ID da lista deve ser um número inteiro positivo.")
        if id_usuario <= 0:
            raise ValueError("O ID do usuário deve ser um número inteiro positivo.")

        lista = self.repositorio.buscar_por_id(id_lista)

        if lista is None:
            return None

        if lista.id_usuario != id_usuario:
            raise PermissionError("Esta lista não pertence ao usuário informado.")

        return lista

    def atualizar_lista(self, id_lista: int, id_usuario: int, nome: str) -> bool:
        if id_lista <= 0:
            raise ValueError("O ID da lista deve ser um número inteiro positivo.")
        if id_usuario <= 0:
            raise ValueError("O ID do usuário deve ser um número inteiro positivo.")

        nome_limpo = nome.strip()
        if not nome_limpo:
            raise ValueError("O nome da lista não pode ficar vazio.")

        if len(nome_limpo) > 100:
            raise ValueError("O nome da lista não pode ultrapassar 100 caracteres.")

        lista = self.repositorio.buscar_por_id(id_lista)

        if lista is None:
            return False

        if lista.id_usuario != id_usuario:
            raise PermissionError("Esta lista não pertence ao usuário informado.")

        lista.nome = nome_limpo
        return self.repositorio.atualizar(lista)

    def excluir_lista(self, id_lista: int, id_usuario: int) -> bool:
        if id_lista <= 0:
            raise ValueError("O ID da lista deve ser um número inteiro positivo.")
        if id_usuario <= 0:
            raise ValueError("O ID do usuário deve ser um número inteiro positivo.")

        lista = self.repositorio.buscar_por_id(id_lista)

        if lista is None:
            return False

        if lista.id_usuario != id_usuario:
            raise PermissionError("Esta lista não pertence ao usuário informado.")

        return self.repositorio.remover(id_lista)