from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import init_db
from app.models.agente import Agente

# IMPORT DA SUA PARTE ISOLADA
from app.api import focos

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando conexão com o MongoDB...")
    await init_db()
    print("Conectado com sucesso!")
    yield
    print("Desligando API...")

app = FastAPI(title="API APP-VIGIAR", lifespan=lifespan)

# PLUGANDO A SUA ROTA "NO SAPATINHO"
# O include_router faz com que o "/focos" do seu arquivo vire "/sync/focos" automaticamente
app.include_router(focos.router, prefix="/sync", tags=["Sincronização"])

@app.get("/")
def read_root():
    return {"status": "API rodando com MongoDB e Beanie!"}

# Rota de teste do Agente (Mantida aqui conforme o seu histórico de testes)
@app.post("/agentes")
async def criar_agente(agente: Agente):
    await agente.insert()
    return {"status": "Agente criado com sucesso!", "dados_salvos": agente}