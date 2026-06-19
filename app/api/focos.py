from fastapi import APIRouter, Query
from typing import List
from beanie.operators import In
from app.models.foco import Foco

router = APIRouter()

# Rota trazida da branch TimoteoBackEnd
# O prefixo "/api/focos" definido no main.py fará esta rota ser acessada em: POST /api/focos
@router.post("")
async def sincronizar_focos(focos_recebidos: List[Foco]):
    # 1. Lista todos os IDs que o celular enviou na rajada
    ids_recebidos = [foco.id_local_celular for foco in focos_recebidos]

    # 2. Trava anti-duplicação: verifica se a nuvem já tem esses dados
    focos_existentes = await Foco.find(In(Foco.id_local_celular, ids_recebidos)).to_list()
    ids_ja_guardados = {foco.id_local_celular for foco in focos_existentes}

    # 3. Filtra apenas os que são realmente novos
    focos_para_inserir = [
        foco for foco in focos_recebidos 
        if foco.id_local_celular not in ids_ja_guardados
    ]

    # 4. Salva tudo de uma vez no MongoDB (alta performance)
    if focos_para_inserir:
        await Foco.insert_many(focos_para_inserir)

    # 5. O "Recibo": junta o que já estava lá com o que acabou de entrar
    ids_sincronizados = list(ids_ja_guardados.union({foco.id_local_celular for foco in focos_para_inserir}))

    return {
        "status": "Sincronização concluída",
        "recebidos": len(focos_recebidos),
        "inseridos_agora": len(focos_para_inserir),
        "ignorados_ja_existentes": len(ids_ja_guardados),
        "ids_seguros_na_nuvem": ids_sincronizados
    }


# Rota trazida da branch main
# Acessível em: GET /api/focos/proximos
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