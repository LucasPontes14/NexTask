from dataclasses import dataclass
from typing import Optional

@dataclass
class Lista:
    id_lista: Optional[int]
    id_usuario: int
    nome: str
    criado_em: Optional[str]