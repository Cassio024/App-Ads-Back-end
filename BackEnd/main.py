from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import init_db
from app.api import focos # Importando suas rotas de focos

# Esta função roda automaticamente quando a API é iniciada
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando conexão com o MongoDB...")
    await init_db() # Isso criará o índice 2dsphere automaticamente
    print("Conectado com sucesso!")
    yield
    print("Desligando API...")

app = FastAPI(title="API APP-VIGIAR", lifespan=lifespan)

# Incluindo suas rotas de focos
app.include_router(focos.router, prefix="/api/focos", tags=["focos"])

@app.get("/")
def read_root():
    return {"status": "API rodando com MongoDB e Beanie!"}