from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from models import ClienteModel, PetModel
from schemas import ClienteCreateSchema, ClienteResponseSchema, ClienteUpdateSchema


router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"],
)


@router.get("/", response_model=List[ClienteResponseSchema], status_code=status.HTTP_200_OK)
def listar_clientes(nome: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(ClienteModel)
    if nome:
        query = query.filter(ClienteModel.nome.contains(nome))
    return query.all()


@router.get("/{cliente_id}", response_model=ClienteResponseSchema, status_code=status.HTTP_200_OK)
def buscar_cliente_por_id(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(ClienteModel).filter(ClienteModel.id == cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado",
        )
    return cliente



def _validar_cpf_unico(cpf: str, db: Session, cliente_id_atual: Optional[int] = None):
    query = db.query(ClienteModel).filter(ClienteModel.cpf == cpf)
    if cliente_id_atual is not None:
        query = query.filter(ClienteModel.id != cliente_id_atual)
    if query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um cliente cadastrado com esse CPF",
        )



def _validar_email_unico(email: str, db: Session, cliente_id_atual: Optional[int] = None):
    query = db.query(ClienteModel).filter(ClienteModel.email == email)
    if cliente_id_atual is not None:
        query = query.filter(ClienteModel.id != cliente_id_atual)
    if query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um cliente cadastrado com esse e-mail",
        )



def _validar_pet_existe(pet_id: int, db: Session):
    pet = db.query(PetModel).filter(PetModel.id == pet_id).first()
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="pet_id informado não existe na tabela de pets",
        )



@router.post("/", response_model=ClienteResponseSchema, status_code=status.HTTP_201_CREATED)
def criar_cliente(dados_cliente: ClienteCreateSchema, db: Session = Depends(get_db)):
    _validar_email_unico(dados_cliente.email, db)
    _validar_cpf_unico(dados_cliente.cpf, db)
    _validar_pet_existe(dados_cliente.pet_id, db)

    novo_cliente = ClienteModel(**dados_cliente.model_dump())
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente



@router.put("/{cliente_id}", response_model=ClienteResponseSchema, status_code=status.HTTP_200_OK)
def atualizar_cliente(cliente_id: int, dados_cliente: ClienteUpdateSchema, db: Session = Depends(get_db)):
    cliente = db.query(ClienteModel).filter(ClienteModel.id == cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado",
        )

    _validar_email_unico(dados_cliente.email, db, cliente_id_atual=cliente_id)
    _validar_cpf_unico(dados_cliente.cpf, db, cliente_id_atual=cliente_id)
    _validar_pet_existe(dados_cliente.pet_id, db)

    for campo, valor in dados_cliente.model_dump().items():
        setattr(cliente, campo, valor)

    db.commit()
    db.refresh(cliente)
    return cliente



@router.delete("/{cliente_id}", status_code=status.HTTP_200_OK)
def deletar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(ClienteModel).filter(ClienteModel.id == cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado",
        )
    try:
        db.delete(cliente)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível remover: existe(m) agendamento(s) vinculado(s) a este cliente",
        )
    return {"mensagem": f"Cliente {cliente_id} removido com sucesso!"}
