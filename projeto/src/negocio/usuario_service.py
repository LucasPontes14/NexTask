from typing import Optional
from src.dados.user_repository import UsuarioRepository
from src.dominio.usuario import Usuario

class UsuarioService:

    def __init__(self, repositorio: UsuarioRepository) -> None:
        self.repositorio = repositorio

    def cadastrar_usuario(self, nome: str, email: str, senha: str) -> Usuario:
        nome_limpo = nome.strip()
        if not nome_limpo: 
            raise ValueError("O nome não pode ficar vazio.")
        if len(nome_limpo) > 100:
            raise ValueError("O nome não pode ultrapassar 100 caracteres.")
        
        email_limpo = email.strip().lower()
        if not email_limpo:
            raise ValueError("O e-mail não pode ficar vazio.")
        if len(email_limpo) > 150:
            raise ValueError("O e-mail não pode ultrapassar 150 caracteres.")
        if "@" not in email_limpo or "." not in email_limpo:
            raise ValueError("O e-mail informado não é válido.")
        if self.repositorio.buscar_por_email(email_limpo) is not None:
            raise ValueError("Já existe um usuário cadastrado com esse e-mail.")

        if not senha:
            raise ValueError("A senha não pode ficar vazia.")
        if len(senha) < 6:
            raise ValueError("A senha deve ter pelo menos 6 caracteres.")
        if len(senha) > 255:
            raise ValueError("A senha não pode ultrapassar 255 caracteres.")

        usuario = Usuario(id_usuario=None, nome=nome_limpo, email=email_limpo, senha=senha, criado_em=None)
        novo_id = self.repositorio.adicionar(usuario)
        usuario.id_usuario = novo_id
        return usuario

    def buscar_usuario_por_id(self, id_usuario: int) -> Optional[Usuario]:
        if id_usuario <= 0:
            raise ValueError("O ID do usuário deve ser um número inteiro positivo.")
        return self.repositorio.buscar_por_id(id_usuario)

    def buscar_usuario_por_email(self, email: str) -> Optional[Usuario]:
        email_limpo = email.strip().lower()
        if not email_limpo:
            raise ValueError("O e-mail não pode ficar vazio.")
        return self.repositorio.buscar_por_email(email_limpo)

    def atualizar_usuario(self, id_usuario: int, nome: str, email: str) -> bool:
        if id_usuario <= 0:
            raise ValueError("O ID do usuário deve ser um número inteiro positivo.")

        nome_limpo = nome.strip()
        if not nome_limpo:
            raise ValueError("O nome não pode ficar vazio.")
        if len(nome_limpo) > 100:
            raise ValueError("O nome não pode ultrapassar 100 caracteres.")

        email_limpo = email.strip().lower()
        if not email_limpo:
            raise ValueError("O e-mail não pode ficar vazio.")
        if len(email_limpo) > 150:
            raise ValueError("O e-mail não pode ultrapassar 150 caracteres.")
        if "@" not in email_limpo or "." not in email_limpo:
            raise ValueError("O e-mail informado não é válido.")

        usuario = self.repositorio.buscar_por_id(id_usuario)
        if usuario is None:
            return False

        dono = self.repositorio.buscar_por_email(email_limpo)
        if dono is not None and dono.id_usuario != id_usuario:
            raise ValueError("Esse e-mail já está sendo usado por outro usuário.")

        usuario.nome = nome_limpo
        usuario.email = email_limpo
        return self.repositorio.atualizar(usuario)
    
    def atualizar_senha(self, id_usuario: int, senha: str, confirmar_senha: str):
        if not senha:
            raise ValueError("A senha não pode ficar vazia.")
        if len(senha)<6:
            raise ValueError("A senha deve possuir mais de 6 caracteres.")
        if len(senha) > 255:
            raise ValueError("A senha não pode ultrapassar 255 caracteres.")
        if senha != confirmar_senha:
            raise ValueError("As senhas não coincidem,")
        usuario = self.repositorio.buscar_por_id(id_usuario)
        usuario.senha = senha
        self.repositorio.atualizar(usuario)

    def excluir_usuario(self, id_usuario: int) -> bool:
        if id_usuario <= 0:
            raise ValueError("O ID do usuário deve ser um número inteiro positivo.")

        usuario = self.repositorio.buscar_por_id(id_usuario)
        if usuario is None:
            return False

        return self.repositorio.remover(id_usuario)