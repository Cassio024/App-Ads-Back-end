from fastapi import APIRouter, Query
from app.models.foco import Foco
from typing import List

router = APIRouter()

@router.get("/proximos", response_model=List[Foco])
async def get_focos_proximos(
    lat: float = Query(...),
    long: float = Query(...),
    raio: int = Query(5000)
):
    # Busca utilizando o índice 2dsphere
    focos = await Foco.find({
        "location": {
            "$nearSphere": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [long, lat]
                },
                "$maxDistance": raio
            }
        }
    }).to_list()
    
    return focos