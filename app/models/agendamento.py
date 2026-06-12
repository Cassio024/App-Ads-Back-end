from beanie import Document
from datetime import datetime

class Agendamento(Document):
    matricula_agente: str
    afazer: str
    horario: str
    status: str = "pendente"  # "pendente" ou "concluido"
    data_criacao: datetime = datetime.utcnow()

    class Settings:
        name = "agendamentos"