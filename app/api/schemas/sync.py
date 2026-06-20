from pydantic import BaseModel
from typing import List, Optional

class ItemVisitaSchema(BaseModel):
    client_id: str
    gps_disponivel: bool
    coordenadas: Optional[List[float]] = None
    registrado_em: str
    status: str
    observacoes: Optional[str] = ""