from fastapi import APIRouter, Query
from typing import List
from beanie.operators import In
from app.models.foco import Foco

# 1. Importando o Schema que acabamos de criar!
from app.api.schemas.focos import FocoSyncSchema

router = APIRouter()

# Rota trazida da branch TimoteoBackEnd
@router.post("")
async def sincronizar_focos(focos_recebidos: List[FocoSyncSchema]): # 2. Recebendo pelo Schema
    # Lista todos os IDs que o celular enviou na rajada
    ids_recebidos = [foco.id_local_celular for foco in focos_recebidos]

    # Trava anti-duplicação: verifica se a nuvem já tem esses dados
    focos_existentes = await Foco.find(In(Foco.id_local_celular, ids_recebidos)).to_list()
    ids_ja_guardados = {foco.id_local_celular for foco in focos_existentes}

    # 3. Filtra e converte o Schema validado para o formato do Banco (Foco)
    focos_para_inserir = [
        Foco(**foco.model_dump()) for foco in focos_recebidos 
        if foco.id_local_celular not in ids_ja_guardados
    ]

    # Salva tudo de uma vez no MongoDB (alta performance)
    if focos_para_inserir:
        await Foco.insert_many(focos_para_inserir)

    # O "Recibo": junta o que já estava lá com o que acabou de entrar
    ids_sincronizados = list(ids_ja_guardados.union({foco.id_local_celular for foco in focos_recebidos}))

    return {
        "status": "Sincronização concluída",
        "recebidos": len(focos_recebidos),
        "inseridos_agora": len(focos_para_inserir),
        "ignorados_ja_existentes": len(ids_ja_guardados),
        "ids_seguros_na_nuvem": ids_sincronizados
    }

# (Pode manter a sua rota @router.get("/proximos") intacta daqui para baixo!)