from pydantic import BaseModel

class AgendamentoCreate(BaseModel):
    matricula_agente: str
    afazer: str
    horario: str