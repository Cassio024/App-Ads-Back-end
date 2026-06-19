# main.py
import os
import uvicorn
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.database import init_db
from app.models.agente import Agente
from contextlib import asynccontextmanager
from app.api import focos
from app.db.database import init_db
from app.api import auth, agendamento, focos

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando conexão com o MongoDB...")
    await init_db()  # Isso criará o banco, as collections e os índices automaticamente
    print("Conectado com sucesso!")
    yield
    print("Desligando API...")

app = FastAPI(title="API APP-VIGIAR", lifespan=lifespan)

# CONFIGURAÇÃO DO CORS: Essencial para o seu PWA conseguir fazer requisições à API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, podes substituir pelo link do seu front no Render
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos de metadados
)

# Incluindo as rotas de focos
app.include_router(focos.router, prefix="/api/focos", tags=["Focos"])

@app.get("/")
def read_root():
    return {"status": "API rodando com MongoDB e Beanie!"}

# Rota de teste do Agente
@app.post("/agentes", tags=["Agentes"])
async def criar_agente(agente: Agente):
    await agente.insert()
    return {"status": "Agente criado com sucesso!", "dados_salvos": agente}

# INICIALIZAÇÃO DINÂMICA: Obrigatório para o Render não dar erro de Port Scan
if __name__ == "__main__":
    # O Render injeta automaticamente a porta correta na variável de ambiente PORT
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)