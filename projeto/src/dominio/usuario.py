from dataclasses import dataclass
from typing import Optional

@dataclass
class Usuario:
    id_usuario: Optional[int]
    nome: str
    email: str
    senha: str
    criado_em: Optional[str]