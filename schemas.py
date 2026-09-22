from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict, Field

from models import PorteEnum




class PetCreateSchema(BaseModel):
    nome: str
    raca: str
    idade: int = Field(ge=0, description="Idade do pet, em anos (não pode ser negativa)")
    porte: PorteEnum  

class PetUpdateSchema(PetCreateSchema):
    pass



class PetResumoSchema(BaseModel):
    id: int
    nome: str
    raca: str
    idade: int
    porte: PorteEnum

    model_config = ConfigDict(from_attributes=True)


class PetResponseSchema(BaseModel):
    id: int
    nome: str
    raca: str
    idade: int
    porte: PorteEnum

    model_config = ConfigDict(from_attributes=True)





class ClienteCreateSchema(BaseModel):
    nome: str
    cpf: int = Field(ge=0, le=99999999999, description="CPF, no máximo 11 dígitos (0 a 99999999999)")
    telefone: int = Field(ge=0, le=99999999999, description="Telefone, no máximo 11 dígitos")
    email: str
    cep: int = Field(ge=0, le=99999999, description="CEP, no máximo 8 dígitos (0 a 99999999)")
    logradouro: str
    numero: int = Field(gt=0, description="Número do endereço, deve ser positivo")
    complemento: str | None = None
    cidade: str
    uf: str
    pet_id: int  


# Usado no PUT: os mesmos dados do Create
class ClienteUpdateSchema(ClienteCreateSchema):
    pass


class ClienteResponseSchema(BaseModel):
    id: int
    nome: str
    cpf: int
    telefone: int
    email: str
    cep: int
    logradouro: str
    numero: int
    complemento: str | None = None
    cidade: str
    uf: str
    pet: PetResumoSchema 

    model_config = ConfigDict(from_attributes=True)


class ClienteResumoComPetSchema(BaseModel):
    id: int
    nome: str
    telefone: int
    email: str
    pet: PetResumoSchema

    model_config = ConfigDict(from_attributes=True)



class FuncionarioCreateSchema(BaseModel):
    nome: str
    cpf: int = Field(ge=0, le=99999999999, description="CPF, no máximo 11 dígitos (0 a 99999999999)")
    telefone: int = Field(ge=0, le=99999999999, description="Telefone, no máximo 11 dígitos")
    email: str
    cep: int = Field(ge=0, le=99999999, description="CEP, no máximo 8 dígitos (0 a 99999999)")
    logradouro: str
    numero: int = Field(gt=0, description="Número do endereço, deve ser positivo")
    complemento: str | None = None
    cidade: str
    uf: str


class FuncionarioUpdateSchema(FuncionarioCreateSchema):
    pass



class FuncionarioResponseSchema(BaseModel):
    id: int
    nome: str
    cpf: int
    telefone: int
    email: str
    cep: int
    logradouro: str
    numero: int
    complemento: str | None = None
    cidade: str
    uf: str

  
    model_config = ConfigDict(from_attributes=True)



class FuncionarioResumoSchema(BaseModel):
    id: int
    nome: str
    email: str
    telefone: int
    cep: int
    logradouro: str
    numero: int
    complemento: str | None = None
    cidade: str
    uf: str

    model_config = ConfigDict(from_attributes=True)


class AgendamentoCreateSchema(BaseModel):
    funcionario_id: int
    cliente_id: int
    servico: str
    data_agendamento: date
    hora_agendamento: time
    observacoes: str | None = None
   


class AgendamentoUpdateSchema(AgendamentoCreateSchema):
    status: str = "Agendado" 

class AgendamentoResponseSchema(BaseModel):
    id: int
    funcionario: FuncionarioResumoSchema
    cliente: ClienteResumoComPetSchema  
    servico: str
    data_agendamento: date
    hora_agendamento: time
    observacoes: str | None = None

    model_config = ConfigDict(from_attributes=True)


class AgendamentoDetalhadoResponseSchema(AgendamentoResponseSchema):
    status: str
