from beanie import Document
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class Location(BaseModel):
    type: str = "Point"
    # Ordem: [longitude, latitude]
    coordinates: List[float]

class Visita(Document):
    id_agente: str
    location: Location
    data: datetime = Field(default_factory=datetime.now)
    status: str  # Ex: "visitada", "fechada"
    observacoes: Optional[str] = None

    class Settings:
        name = "visitas"
        indexes = [
            [("location", "2dsphere")],
            "id_agente",
            "status",
            "data"
        ]