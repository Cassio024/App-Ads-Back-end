from pydantic import BaseModel

class FocoSyncSchema(BaseModel):
    id_local_celular: str
    latitude: float
    longitude: float
    quantidade_focos: int
    # Se enviar mais coisas do front-end, pode adicionar aqui!