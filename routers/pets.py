from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from models import PetModel
from schemas import PetCreateSchema, PetResponseSchema, PetUpdateSchema


router = APIRouter(
    prefix="/pets",
    tags=["Pets"],
)


@router.get("/", response_model=List[PetResponseSchema], status_code=status.HTTP_200_OK)
def listar_pets(nome: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(PetModel)
    if nome:
        query = query.filter(PetModel.nome.contains(nome))
    return query.all()


@router.get("/{pet_id}", response_model=PetResponseSchema, status_code=status.HTTP_200_OK)
def buscar_pet_por_id(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(PetModel).filter(PetModel.id == pet_id).first()
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet não encontrado",
        )
    return pet



@router.post("/", response_model=PetResponseSchema, status_code=status.HTTP_201_CREATED)
def criar_pet(dados_pet: PetCreateSchema, db: Session = Depends(get_db)):
    novo_pet = PetModel(**dados_pet.model_dump())
    db.add(novo_pet)
    db.commit()
    db.refresh(novo_pet)
    return novo_pet



@router.put("/{pet_id}", response_model=PetResponseSchema, status_code=status.HTTP_200_OK)
def atualizar_pet(pet_id: int, dados_pet: PetUpdateSchema, db: Session = Depends(get_db)):
    pet = db.query(PetModel).filter(PetModel.id == pet_id).first()
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet não encontrado",
        )

    for campo, valor in dados_pet.model_dump().items():
        setattr(pet, campo, valor)

    db.commit()
    db.refresh(pet)
    return pet



@router.delete("/{pet_id}", status_code=status.HTTP_200_OK)
def deletar_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(PetModel).filter(PetModel.id == pet_id).first()
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet não encontrado",
        )
    try:
        db.delete(pet)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível remover: existe(m) cliente(s) vinculado(s) a este pet",
        )
    return {"mensagem": f"Pet {pet_id} removido com sucesso!"}
