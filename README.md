# PetShop API

## Descrição

API para gerenciamento de um **Pet Shop**. O sistema controla os **clientes** (donos dos animais), os **funcionários** do petshop, os **pets** e os **agendamentos** de serviços, permitindo o CRUD completo de todas as entidades.

## Entidades

### `pets`

Entidade independente — não referencia nenhuma outra tabela.

| Campo | Tipo   | Descrição                    |
|-------|--------|--------------------------------|
| id    | int    | Identificador único            |
| nome  | string | Nome do pet                    |
| raca  | string | Raça do pet                    |
| idade | int    | Idade do pet, em anos (≥ 0)    |
| porte | enum   | PEQUENO, MEDIO ou GRANDE       |

### `clientes`

Cadastro completo de uma pessoa (o dono do pet), sem senha — não há login/autenticação, apenas dados de contato, endereço e o `pet_id` do pet que já deve estar cadastrado.

| Campo       | Tipo   | Descrição                                      |
|-------------|--------|---------------------------------------------------|
| id          | int    | Identificador único                                |
| nome        | string | Nome do cliente                                    |
| cpf         | string | CPF (11 dígitos, único)                            |
| telefone    | string | Telefone de contato                                |
| email       | string | E-mail de contato (único)                          |
| cep         | string | CEP (8 dígitos)                                    |
| logradouro  | string | Rua/avenida                                        |
| numero      | int    | Número do endereço                                 |
| complemento | string | Complemento (opcional)                             |
| cidade      | string | Cidade                                              |
| uf          | string | Estado (UF)                                        |
| pet_id      | int    | Chave estrangeira — referência a um `pets.id` já existente |

> Repare que a chave estrangeira fica no **cliente**, não no pet: é o cliente que aponta para o pet, e não o contrário. Por isso um Pet precisa existir **antes** de cadastrar o Cliente.

### `funcionarios`

Colaboradores do petshop, responsáveis por atender os agendamentos. Entidade independente, sem vínculo com pets ou clientes.

| Campo       | Tipo   | Descrição                          |
|-------------|--------|--------------------------------------|
| id          | int    | Identificador único                  |
| nome        | string | Nome do funcionário                  |
| cpf         | string | CPF (11 dígitos, único)              |
| telefone    | string | Telefone de contato                  |
| email       | string | E-mail de contato                    |
| cep         | string | CEP (8 dígitos)                      |
| logradouro  | string | Rua/avenida                          |
| numero      | int    | Número do endereço                   |
| complemento | string | Complemento (opcional)               |
| cidade      | string | Cidade                               |
| uf          | string | Estado (UF)                          |

### `agendamentos`

| Campo           | Tipo   | Descrição                                          |
|-----------------|--------|-------------------------------------------------------|
| id              | int    | Identificador único                                   |
| funcionario_id  | int    | Chave estrangeira — referência a `funcionarios.id`    |
| cliente_id      | int    | Chave estrangeira — referência a `clientes.id`        |
| servico         | string | Ex: Banho, Tosa, Consulta veterinária                 |
| data_agendamento| date   | Data do agendamento                                   |
| hora_agendamento| time   | Hora do agendamento                                   |
| status          | string | Agendado / Concluído / Cancelado (oculto na resposta padrão) |
| observacoes     | string | Observações (opcional)                                |

> O agendamento aponta para o **cliente**, não mais direto para o pet. Como o cliente já carrega o `pet_id` dele, a resposta do agendamento mostra o cliente com o pet aninhado dentro dele (`cliente.pet`), então dá pra ver as informações do pet relacionado ao cliente direto na tela.

## Ordem de criação (por causa das dependências)

1. **Pet** (não depende de nada)
2. **Funcionário** (não depende de nada)
3. **Cliente** (precisa de um `pet_id` já existente)
4. **Agendamento** (precisa de um `funcionario_id` e um `cliente_id` já existentes)

O banco tem checagem de chaves estrangeiras habilitada (`PRAGMA foreign_keys=ON`), então não é possível excluir um Pet que ainda tenha um Cliente apontando para ele, nem excluir um Funcionário ou Cliente que ainda tenha Agendamentos vinculados — a API retorna erro 400 nesses casos.

## Contrato das Rotas HTTP

| Método | Rota                  | Descrição                                                    |
|--------|-----------------------|-------------------------------------------------------------|
| GET    | `/`                   | Mensagem de status da API                                    |
| GET    | `/pets`               | Lista todos os pets (aceita `?nome=` para busca)              |
| GET    | `/pets/seed`          | Cria um pet de exemplo com dados aleatórios (JSON)            |
| GET    | `/pets/{id}`          | Retorna um pet específico pelo id                             |
| POST   | `/pets`               | Cadastra um novo pet                                          |
| PUT    | `/pets/{id}`          | Atualiza um pet existente                                     |
| DELETE | `/pets/{id}`          | Remove um pet (falha se houver cliente vinculado)             |
| GET    | `/clientes`           | Lista todos os clientes (aceita `?nome=` para busca)          |
| GET    | `/clientes/seed`      | Cria um cliente de exemplo (cria um pet se não houver nenhum) |
| GET    | `/clientes/{id}`      | Retorna um cliente específico pelo id                         |
| POST   | `/clientes`           | Cadastra um novo cliente (requer `pet_id` existente)          |
| PUT    | `/clientes/{id}`      | Atualiza um cliente existente                                 |
| DELETE | `/clientes/{id}`      | Remove um cliente (falha se houver agendamento vinculado)     |
| GET    | `/funcionarios`       | Lista todos os funcionários (aceita `?nome=` para busca)      |
| GET    | `/funcionarios/seed`  | Cria um funcionário de exemplo com dados aleatórios (JSON)    |
| GET    | `/funcionarios/{id}`  | Retorna um funcionário específico pelo id                     |
| POST   | `/funcionarios`       | Cadastra um novo funcionário                                  |
| PUT    | `/funcionarios/{id}`  | Atualiza um funcionário existente                             |
| DELETE | `/funcionarios/{id}`  | Remove um funcionário                                         |
| GET    | `/agendamentos`       | Lista agendamentos (aceita `?status_filtro=` e `?completo=`)  |
| GET    | `/agendamentos/seed`  | Cria um agendamento de exemplo (cria funcionário/cliente se faltar)|
| GET    | `/agendamentos/{id}`  | Retorna um agendamento específico pelo id                     |
| POST   | `/agendamentos`       | Cadastra um novo agendamento                                  |
| PUT    | `/agendamentos/{id}`  | Atualiza um agendamento existente                             |
| DELETE | `/agendamentos/{id}`  | Remove um agendamento                                         |

As rotas `/seed` existem só para facilitar testes manuais: cada chamada `GET` cria um registro novo com dados de exemplo (CPF/e-mail/CEP aleatórios, para não colidir com os campos `unique`) e devolve o objeto criado em JSON.

## Arquitetura

Arquitetura em camadas, com persistência real em SQLite via SQLAlchemy:

```
Pet-shop/
├── main.py                    # instância do FastAPI, inclui os routers e a rota raiz
├── database.py                # conexão SQLAlchemy/SQLite (engine, SessionLocal, Base, get_db)
├── models.py                  # modelos SQLAlchemy (PetModel, ClienteModel, FuncionarioModel, AgendamentoModel)
├── schemas.py                 # schemas Pydantic de entrada/saída
├── pet.db                      # banco SQLite local (já criado, com as tabelas vazias)
├── routers/
│   ├── pets.py                 # endpoints do CRUD de Pet (+ /pets/seed e criar_pet_exemplo/obter_ou_criar_pet)
│   ├── clientes.py             # endpoints do CRUD de Cliente (+ /clientes/seed e criar_cliente_exemplo/obter_ou_criar_cliente; reaproveita obter_ou_criar_pet)
│   ├── funcionarios.py         # endpoints do CRUD de Funcionario (+ /funcionarios/seed e criar_funcionario_exemplo/obter_ou_criar_funcionario)
│   └── agendamentos.py         # endpoints do CRUD de Agendamento (+ /agendamentos/seed, reaproveita obter_ou_criar_cliente e obter_ou_criar_funcionario)
├── .gitignore
└── README.md
```

As funções auxiliares de seed (`criar_pet_exemplo`/`obter_ou_criar_pet`, `criar_funcionario_exemplo`/`obter_ou_criar_funcionario`, `criar_cliente_exemplo`/`obter_ou_criar_cliente`) moram nos próprios routers de Pet, Funcionario e Cliente — não existe um arquivo utilitário separado. O router de Agendamento simplesmente importa as que precisa (`from routers.clientes import obter_ou_criar_cliente`, `from routers.funcionarios import obter_ou_criar_funcionario`), já que essa dependência entre as entidades já existe naturalmente.

## Como executar

```bash
pip install fastapi uvicorn sqlalchemy pydantic
fastapi dev main.py
```

Depois acesse `http://127.0.0.1:8000/docs` para testar os endpoints pelo Swagger.

O arquivo `pet.db` já vem criado neste projeto (com as tabelas no schema atual, mas vazias). Se preferir começar do zero, basta apagá-lo: ele é recriado automaticamente na próxima execução (`Base.metadata.create_all` em `main.py`).
