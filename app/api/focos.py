from fastapi import APIRouter
from typing import List
from beanie.operators import In
from app.models.foco import Foco

router = APIRouter()

# Reparou que aqui usamos apenas "/focos"? 
# O prefixo "/sync" será definido no main.py para manter a rota original.
@router.post("/focos")
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