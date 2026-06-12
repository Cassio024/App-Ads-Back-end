from fastapi import APIRouter, HTTPException, status
from app.models.agendamento import Agendamento
from app.models.usuario import Usuario
from app.api.schemas.agendamento import AgendamentoCreate
from typing import List

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])

@router.post("/criar")
async def criar_tarefa(payload: AgendamentoCreate):
    # Verifica se o agente realmente existe no banco
    agente = await Usuario.find_one(Usuario.matricula == payload.matricula_agente, Usuario.tipo == "agente")
    if not agente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum Agente de Saúde foi localizado com esta matrícula."
        )

    nova_tarefa = Agendamento(
        matricula_agente=payload.matricula_agente,
        afazer=payload.afazer,
        horario=payload.horario,
        status="pendente"
    )
    await nova_tarefa.insert()
    return {"message": "Tarefa atribuída com sucesso!"}

@router.get("/todos", response_model=List[Agendamento])
async def listar_todos():
    return await Agendamento.find_all().to_list()

@router.get("/agente/{matricula}", response_model=List[Agendamento])
async def listar_por_agente(matricula: str):
    return await Agendamento.find(Agendamento.matricula_agente == matricula).to_list()

@router.patch("/{id_tarefa}/concluir")
async def concluir_tarefa(id_tarefa: str):
    tarefa = await Agendamento.get(id_tarefa)
    if not tarefa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada."
        )
    tarefa.status = "concluido"
    await tarefa.save()
    return {"message": "Tarefa dada como concluída com sucesso!"}