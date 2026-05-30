from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import init_db

# --- NOVOS IMPORTS ADICIONADOS ---
from typing import List
from beanie.operators import In
from app.models.foco import Foco
# ---------------------------------

# Esta função roda automaticamente quando a API é iniciada
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando conexão com o MongoDB...")
    await init_db()
    print("Conectado com sucesso!")
    yield
    print("Desligando API...")

app = FastAPI(title="API APP-VIGIAR", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"status": "API rodando com MongoDB e Beanie!"}

# --- NOVA ROTA ADICIONADA AQUI NO FINAL ---
@app.post("/sync/focos")
async def sincronizar_focos(focos_recebidos: List[Foco]):
    # Pega os IDs que vieram do aplicativo
    ids_recebidos = [foco.id_local_celular for foco in focos_recebidos]

    # Procura no banco quais desses IDs já existem
    focos_existentes = await Foco.find(In(Foco.id_local_celular, ids_recebidos)).to_list()
    ids_ja_guardados = {foco.id_local_celular for foco in focos_existentes}

    # Separa apenas os que são novidade
    focos_para_inserir = [
        foco for foco in focos_recebidos 
        if foco.id_local_celular not in ids_ja_guardados
    ]

    # Salva os novos no banco
    if focos_para_inserir:
        await Foco.insert_many(focos_para_inserir)

    # Devolve o resumo da operação
    return {
        "status": "Sincronização concluída",
        "recebidos": len(focos_recebidos),
        "inseridos_agora": len(focos_para_inserir),
        "ignorados_ja_existentes": len(ids_ja_guardados)
    }