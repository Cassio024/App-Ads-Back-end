from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import init_db
from app.models.agente import Agente
from app.api import focos

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando conexão com o MongoDB...")
    await init_db()  # Isso criará o índice 2dsphere automaticamente
    print("Conectado com sucesso!")
    yield
    print("Desligando API...")

app = FastAPI(title="API APP-VIGIAR", lifespan=lifespan)

# Incluindo as rotas de focos
app.include_router(focos.router, prefix="/api/focos", tags=["Focos"])

@app.get("/")
def read_root():
    return {"status": "API rodando com MongoDB e Beanie!"}

# Rota de teste do Agente (Mantida da branch TimoteoBackEnd)
@app.post("/agentes", tags=["Agentes"])
async def criar_agente(agente: Agente):
    await agente.insert()
    return {"status": "Agente criado com sucesso!", "dados_salvos": agente}