from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from app.api.schemas.auth import LoginSchema, RegisterSchema
from app.models.usuario import Usuario
import bcrypt

router = APIRouter(prefix="/auth", tags=["Autenticação"])

# Novo Schema para a validação da atualização de perfil
class UpdateProfileSchema(BaseModel):
    nome: str
    foto_base64: Optional[str] = None

@router.post("/register")
async def register(payload: RegisterSchema):
    # Verifica se o usuário já existe
    usuario_existente = await Usuario.find_one(Usuario.matricula == payload.matricula)
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta matrícula já está cadastrada no sistema."
        )
    
    if not payload.foto_base64 or payload.foto_base64.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A foto de perfil em formato de captura de rosto é obrigatória."
        )

    # Criptografia segura da senha
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(payload.password.encode('utf-8'), salt).decode('utf-8')
    
    novo_usuario = Usuario(
        matricula=payload.matricula,
        nome=payload.nome,
        senha_hash=senha_hash,
        tipo=payload.tipo,
        foto_base64=payload.foto_base64
    )
    await novo_usuario.insert()
    return {"message": "Cadastro realizado com sucesso!"}

@router.post("/login")
async def login(payload: LoginSchema):
    # Busca o usuário validando a matrícula e o tipo de conta escolhido
    usuario = await Usuario.find_one(Usuario.matricula == payload.matricula, Usuario.tipo == payload.tipo)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Matrícula ou tipo de conta incorretos."
        )
    
    # Compara o hash da senha enviada com a do banco
    if not bcrypt.checkpw(payload.password.encode('utf-8'), usuario.senha_hash.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha incorreta."
        )
    
    return {
        "user": {
            "matricula": usuario.matricula,
            "nome": usuario.nome,
            "tipo": usuario.tipo,
            "foto_base64": usuario.foto_base64
        }
    }

# ==========================================
# NOVAS ROTAS DE CONFIGURAÇÃO DE PERFIL
# ==========================================

@router.patch("/update/{matricula}")
async def update_profile(matricula: str, payload: UpdateProfileSchema):
    # Busca o usuário no banco
    usuario = await Usuario.find_one(Usuario.matricula == matricula)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )
    
    # Atualiza o nome e, se fornecida, a foto
    usuario.nome = payload.nome
    if payload.foto_base64 and payload.foto_base64.strip() != "":
        usuario.foto_base64 = payload.foto_base64
        
    await usuario.save()
    return {"message": "Perfil atualizado com sucesso!"}

@router.delete("/delete/{matricula}")
async def delete_profile(matricula: str):
    # Busca o usuário no banco
    usuario = await Usuario.find_one(Usuario.matricula == matricula)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado."
        )
    
    # Exclui o registro permanentemente
    await usuario.delete()
    return {"message": "Conta excluída com sucesso!"}