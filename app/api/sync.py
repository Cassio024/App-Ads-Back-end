from fastapi import APIRouter, status
from typing import List
from app.api.schemas.sync import ItemVisitaSchema
from app.models.visitas import Visita, Location
from datetime import datetime

router = APIRouter(prefix="/sync", tags=["Sincronização"])

@router.post("")
async def sincronizar_dados(payload: List[ItemVisitaSchema]):
    ids_confirmados = []
    
    for item in payload:
        try:
            # Converte a estrutura que veio do celular para a estrutura do banco Beanie (visitas.py)
            nova_visita = Visita(
                id_agente="sistema_offline",  # Ajustável conforme o login
                location=Location(
                    type="Point",
                    coordinates=item.coordenadas if item.gps_disponivel and item.coordenadas else [0.0, 0.0]
                ),
                data=datetime.fromisoformat(item.registrado_em.replace("Z", "+00:00")),
                status=item.status,
                observacoes=item.observacoes
            )
            
            # Salva direto no MongoDB de forma assíncrona
            await nova_visita.insert()
            
            # Se salvou com sucesso, adiciona na lista de confirmação
            ids_confirmados.append(item.client_id)
            
        except Exception as e:
            print(f"Erro ao processar a visita {item.client_id}: {str(e)}")
            continue
            
    return {
        "status": "success",
        "synchronized_ids": ids_confirmados
    }