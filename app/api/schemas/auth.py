from pydantic import BaseModel

class LoginSchema(BaseModel):
    matricula: str
    password: str
    tipo: str

class RegisterSchema(BaseModel):
    nome: str
    matricula: str
    password: str
    tipo: str
    foto_base64: str