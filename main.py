from fastapi import FastAPI

from database import Base, engine
from routers import agendamentos, clientes, funcionarios, pets


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PetShop API",
    description="API para cadastro e consulta de clientes, pets e funcionários",
)

app.include_router(funcionarios.router)
app.include_router(pets.router)
app.include_router(clientes.router)
app.include_router(agendamentos.router)


@app.get("/")
def home():
    return {"mensagem": "PetShop API rodando com sucesso"}
