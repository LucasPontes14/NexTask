import mysql.connector

from interface.login_screen import TelaLogin
from interface.main_screen import TelaPrincipal
from src.dados.user_repository import UsuarioRepository
from src.negocio.usuario_service import UsuarioService
from src.dados.list_repository import ListRepository
from src.negocio.lista_service import ListaService
from src.dados.tarefa_repository import TaskRepository
from src.negocio.tarefa_service import TarefaService

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Debora091403#",
    database="db_tarefas"
)

usuario_repo = UsuarioRepository(conexao)
lista_repo   = ListRepository(conexao)
tarefa_repo  = TaskRepository(conexao)

usuario_service = UsuarioService(usuario_repo)
lista_service   = ListaService(lista_repo)
tarefa_service  = TarefaService(tarefa_repo)

app = TelaLogin(usuario_service, lista_service, tarefa_service)
app.mainloop()