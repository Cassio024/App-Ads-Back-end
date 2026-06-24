import os
import certifi # <-- 1. Importação do pacote de certificados adicionada
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.models.usuario import Usuario
from app.models.agendamento import Agendamento
from app.models.foco import Foco
from typing import Any, cast

async def init_db():
    database_url = getattr(settings, "DATABASE_URL", None) or os.getenv("MONGO_URI") or os.getenv("DATABASE_URL")
    
    if not database_url:
        raise ValueError(
            "ERRO: A URL de conexão com o MongoDB não foi encontrada!\n"
            "Certifique-se de definir 'DATABASE_URL' ou 'MONGO_URI' no seu arquivo .env ou no Render."
        )

    # <-- 2. Adicionado o parâmetro tlsCAFile apontando para o certifi
    client = AsyncIOMotorClient(database_url, tlsCAFile=certifi.where())
    
    try:
        database = client.get_default_database()
        if database is None or database.name == "test":
            database = client.app_ecovetor
    except Exception:
        database = client.app_ecovetor
    
    # Inicializa o Beanie mapeando todos os modelos ativos do sistema
    await init_beanie(
        database=cast(Any, database),
        document_models=[Usuario, Agendamento, Foco]
    )