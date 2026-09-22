from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import FuncionarioModel
from schemas import FuncionarioCreateSchema, FuncionarioResponseSchema, FuncionarioUpdateSchema


router = APIRouter(
    prefix="/funcionarios",
    tags=["Funcionários"],
)



@router.get("/", response_model=List[FuncionarioResponseSchema], status_code=status.HTTP_200_OK)
def listar_funcionarios(nome: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(FuncionarioModel)
    if nome:
        query = query.filter(FuncionarioModel.nome.contains(nome))
    return query.all()


@router.get("/{funcionario_id}", response_model=FuncionarioResponseSchema, status_code=status.HTTP_200_OK)
def buscar_funcionario_por_id(funcionario_id: int, db: Session = Depends(get_db)):
    funcionario = db.query(FuncionarioModel).filter(FuncionarioModel.id == funcionario_id).first()
    if not funcionario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado",
        )
    return funcionario


def _validar_cpf_unico(cpf: str, db: Session, funcionario_id_atual: Optional[int] = None):
    query = db.query(FuncionarioModel).filter(FuncionarioModel.cpf == cpf)
    if funcionario_id_atual is not None:
        query = query.filter(FuncionarioModel.id != funcionario_id_atual)
    if query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um funcionário cadastrado com esse CPF",
        )



@router.post("/", response_model=FuncionarioResponseSchema, status_code=status.HTTP_201_CREATED)
def criar_funcionario(dados_funcionario: FuncionarioCreateSchema, db: Session = Depends(get_db)):
    _validar_cpf_unico(dados_funcionario.cpf, db)

    novo_funcionario = FuncionarioModel(**dados_funcionario.model_dump())
    db.add(novo_funcionario)
    db.commit()
    db.refresh(novo_funcionario)
    return novo_funcionario



@router.put("/{funcionario_id}", response_model=FuncionarioResponseSchema, status_code=status.HTTP_200_OK)
def atualizar_funcionario(
    funcionario_id: int, dados_funcionario: FuncionarioUpdateSchema, db: Session = Depends(get_db)
):
    funcionario = db.query(FuncionarioModel).filter(FuncionarioModel.id == funcionario_id).first()
    if not funcionario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado",
        )

    _validar_cpf_unico(dados_funcionario.cpf, db, funcionario_id_atual=funcionario_id)

    for campo, valor in dados_funcionario.model_dump().items():
        setattr(funcionario, campo, valor)

    db.commit()
    db.refresh(funcionario)
    return funcionario



@router.delete("/{funcionario_id}", status_code=status.HTTP_200_OK)
def deletar_funcionario(funcionario_id: int, db: Session = Depends(get_db)):
    funcionario = db.query(FuncionarioModel).filter(FuncionarioModel.id == funcionario_id).first()
    if not funcionario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado",
        )
    db.delete(funcionario)
    db.commit()
    return {"mensagem": f"Funcionário {funcionario_id} removido com sucesso!"}
