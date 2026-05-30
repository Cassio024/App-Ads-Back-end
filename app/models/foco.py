from beanie import Document
from typing import Dict, Any, List
from pydantic import BaseModel

class Location(BaseModel):
    type: str = "Point"
    # Ordem: [longitude, latitude]
    coordinates: List[float]

class Foco(Document):
    id_visita: str
    tipo_criadouro: str
    acao_tomada: str
    id_local_celular: str
    latitude: float
    longitude: float
    location: Location
    dados_coletados: Dict[str, Any]
    timestamp: str

    class Settings:
        name = "focos"
        indexes = [
            [("location", "2dsphere")]
        ]