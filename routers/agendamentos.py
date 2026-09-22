from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import get_db
from models import AgendamentoModel, ClienteModel, FuncionarioModel
from schemas import (
    AgendamentoCreateSchema,
    AgendamentoDetalhadoResponseSchema,
    AgendamentoResponseSchema,
    AgendamentoUpdateSchema,
)


router = APIRouter(
    prefix="/agendamentos",
    tags=["Agendamentos"],
)



def _validar_funcionario_e_cliente(funcionario_id: int, cliente_id: int, db: Session):
    if not db.query(FuncionarioModel).filter(FuncionarioModel.id == funcionario_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="funcionario_id informado não existe",
        )
    if not db.query(ClienteModel).filter(ClienteModel.id == cliente_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="cliente_id informado não existe",
        )


def _serializar_agendamento(agendamento: AgendamentoModel, completo: bool):
    schema_cls = AgendamentoDetalhadoResponseSchema if completo else AgendamentoResponseSchema
    return schema_cls.model_validate(agendamento)



@router.get(
    "/",
    response_model=None,  
    status_code=status.HTTP_200_OK,
)
def listar_agendamentos(
    status_filtro: Optional[str] = None,
    completo: bool = Query(False, description="Se true, inclui o campo 'status' na resposta"),
    db: Session = Depends(get_db),
):
    query = db.query(AgendamentoModel)
    if status_filtro:
        query = query.filter(AgendamentoModel.status == status_filtro)
    agendamentos = query.all()
    return [_serializar_agendamento(a, completo) for a in agendamentos]



@router.get(
    "/{agendamento_id}",
    response_model=None, 
    status_code=status.HTTP_200_OK,
)
def buscar_agendamento_por_id(
    agendamento_id: int,
    completo: bool = Query(False, description="Se true, inclui o campo 'status' na resposta"),
    db: Session = Depends(get_db),
):
    agendamento = db.query(AgendamentoModel).filter(AgendamentoModel.id == agendamento_id).first()
    if not agendamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agendamento não encontrado",
        )
    return _serializar_agendamento(agendamento, completo)



@router.post(
    "/",
    response_model=None,  
    status_code=status.HTTP_201_CREATED,
)
def criar_agendamento(
    dados_agendamento: AgendamentoCreateSchema,
    completo: bool = Query(False, description="Se true, inclui o campo 'status' na resposta"),
    db: Session = Depends(get_db),
):
    _validar_funcionario_e_cliente(dados_agendamento.funcionario_id, dados_agendamento.cliente_id, db)

    
    novo_agendamento = AgendamentoModel(**dados_agendamento.model_dump(), status="Agendado")
    db.add(novo_agendamento)
    db.commit()
    db.refresh(novo_agendamento)
    return _serializar_agendamento(novo_agendamento, completo)



@router.put(
    "/{agendamento_id}",
    response_model=None,  
    status_code=status.HTTP_200_OK,
)
def atualizar_agendamento(
    agendamento_id: int,
    dados_agendamento: AgendamentoUpdateSchema,
    completo: bool = Query(False, description="Se true, inclui o campo 'status' na resposta"),
    db: Session = Depends(get_db),
):
    agendamento = db.query(AgendamentoModel).filter(AgendamentoModel.id == agendamento_id).first()
    if not agendamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agendamento não encontrado",
        )

    _validar_funcionario_e_cliente(dados_agendamento.funcionario_id, dados_agendamento.cliente_id, db)

    for campo, valor in dados_agendamento.model_dump().items():
        setattr(agendamento, campo, valor)

    db.commit()
    db.refresh(agendamento)
    return _serializar_agendamento(agendamento, completo)



@router.delete("/{agendamento_id}", status_code=status.HTTP_200_OK)
def deletar_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    agendamento = db.query(AgendamentoModel).filter(AgendamentoModel.id == agendamento_id).first()
    if not agendamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agendamento não encontrado",
        )
    db.delete(agendamento)
    db.commit()
    return {"mensagem": f"Agendamento {agendamento_id} removido com sucesso!"}
