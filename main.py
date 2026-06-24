import os
import uvicorn
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Importações dos seus módulos
from app.db.database import init_db
from app.api import auth, agendamento, focos, sync
from app.models.agente import Agente

load_dotenv(find_dotenv())

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando conexão com o MongoDB...")
    await init_db() 
    print("Conectado com sucesso!")
    yield
    print("Desligando API...")

app = FastAPI(title="API APP-VIGIAR", lifespan=lifespan)

# CONFIGURAÇÃO DO CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REGISTRO DE ROTAS
app.include_router(auth.router)           
app.include_router(sync.router)           
app.include_router(agendamento.router) # Sem prefixo aqui (já está em app/api/agendamento.py)

# O de focos precisa do prefixo aqui de volta para evitar o erro de path vazio!
# Se o seu frontend antigo chamava "/api/focos", você pode usar prefix="/api/focos".
# Se preferir o padrão limpo igual aos outros, use prefix="/focos".
app.include_router(focos.router, prefix="/focos", tags=["Focos"]) 

@app.get("/")
def read_root():
    return {"status": "API rodando com MongoDB e Beanie!"}