from dataclasses import dataclass
from typing import Optional

class Tarefa:
    id_tarefa: Optional[int]
    id_lista: int
    titulo: str
    descricao: str
    prioridade: str
    status: str
    data_venc: str
    hora_venc: str
    criado_em: Optional[str]