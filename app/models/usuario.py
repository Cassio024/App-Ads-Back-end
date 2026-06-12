from beanie import Document
from typing import Optional

class Usuario(Document):
    matricula: str
    nome: str
    senha_hash: str
    tipo: str  # "agente" ou "secretario"
    foto_base64: Optional[str] = None
    ativo: bool = True

    class Settings:
        name = "usuarios"