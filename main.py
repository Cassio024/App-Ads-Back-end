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
# Deixamos o FastAPI usar apenas os prefixos que já estão definidos dentro de cada arquivo!
app.include_router(auth.router)           
app.include_router(sync.router)           
app.include_router(focos.router)          
app.include_router(agendamento.router)    

@app.get("/")
def read_root():
    return {"status": "API rodando com MongoDB e Beanie!"}