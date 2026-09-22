import enum

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    String,
    Time,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base



class PorteEnum(str, enum.Enum):
    PEQUENO = "PEQUENO"
    MEDIO = "MEDIO"
    GRANDE = "GRANDE"


class FuncionarioModel(Base):
    __tablename__ = "funcionarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False, index=True)
    cpf = Column(Integer, nullable=False, unique=True, index=True)
    telefone = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    cep = Column(Integer, nullable=False)
    logradouro = Column(String, nullable=False)
    numero = Column(Integer, nullable=False)
    complemento = Column(String, nullable=True)  
    cidade = Column(String, nullable=False)
    uf = Column(String, nullable=False)

    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

   


class PetModel(Base):
    __tablename__ = "pets" 

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False, index=True)
    raca = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)  
    porte = Column(SqlEnum(PorteEnum), nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

 


class ClienteModel(Base):
    __tablename__ = "clientes" 

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False, index=True)
    cpf = Column(Integer, nullable=False, unique=True, index=True)
    telefone = Column(Integer, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    cep = Column(Integer, nullable=False)
    logradouro = Column(String, nullable=False)
    numero = Column(Integer, nullable=False)
    complemento = Column(String, nullable=True) 
    cidade = Column(String, nullable=False)
    uf = Column(String, nullable=False)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    pet = relationship("PetModel")


class AgendamentoModel(Base):
    __tablename__ = "agendamentos" 

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    servico = Column(String, nullable=False) 
    data_agendamento = Column(Date, nullable=False)
    hora_agendamento = Column(Time, nullable=False)
    status = Column(String, nullable=False, default="Agendado")  
    observacoes = Column(String, nullable=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    funcionario = relationship("FuncionarioModel")
    cliente = relationship("ClienteModel")
