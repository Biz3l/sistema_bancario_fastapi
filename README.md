# Sistema Bancario com FastAPI

API de estudo para simulacao de operacoes bancarias basicas, desenvolvida com FastAPI.

> Projeto criado como estudo para a **Luizalabs** na plataforma **DIO (Digital Innovation One)**.

## Visao geral

Este projeto implementa um mini sistema bancario com:

- Criacao e listagem de usuarios
- Login com JWT
- Consulta de saldo
- Deposito
- Saque
- Transferencia entre usuarios
- Extrato de transacoes

A ideia foi praticar organizacao em camadas, autenticacao e manipulacao de dados com SQLite.

## Stack utilizada

- Python 3.13+
- FastAPI
- Uvicorn
- SQLAlchemy
- Databases
- SQLite
- PyJWT
- Poetry

## Estrutura do projeto

```text
.
├── main.py                 # Inicializa a aplicacao e registra os routers
├── database.py             # Conexao com SQLite, metadata e engine
├── security.py             # Geracao/validacao de JWT e protecao de rotas
├── controllers/            # Endpoints da API
├── services/               # Regras de negocio
├── models/                 # Definicao das tabelas
├── schemas/                # Contratos de entrada (request)
└── views/                  # Contratos de saida (response)
```

## Como executar localmente

### 1. Clonar o repositorio

```bash
git clone https://github.com/Biz3l/sistema_bancario_fastapi.git
cd sistema_bancario_fastapi
```

### 2. Instalar dependencias

```bash
poetry install
```

### 3. Iniciar a API

```bash
poetry run uvicorn main:app --reload
```

A API ficara disponivel em:

- `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Fluxo rapido de uso

### 1. Criar usuario

`POST /user/createuser`

```json
{
  "name": "Gabriel"
}
```

### 2. Fazer login

`POST /auth/login`

```json
{
  "user_id": 1
}
```

Resposta esperada:

```json
{
  "access_token": "seu_token_jwt"
}
```

### 3. Chamar rotas protegidas

Envie o token no header:

```text
Authorization: Bearer seu_token_jwt
```

Rotas protegidas:

- `GET /balance/`
- `POST /bank/deposit`
- `POST /bank/withdraw`
- `POST /bank/transfer`
- `GET /bank/statement`

## Endpoints principais

### Usuarios

- `GET /user/` - lista usuarios
- `POST /user/createuser` - cria usuario com saldo inicial 0

### Autenticacao

- `POST /auth/login` - gera JWT a partir do `user_id`

### Operacoes bancarias (protegidas)

- `GET /balance` - retorna saldo atual
- `POST /bank/deposit` - realiza deposito
- `POST /bank/withdraw` - realiza saque
- `POST /bank/transfer` - transfere para outro usuario
- `GET /bank/statement` - lista extrato

## Objetivo de aprendizado

Este projeto foi usado para praticar:

- Estruturacao de API com separacao de responsabilidades
- Autenticacao via JWT em rotas protegidas
- Operacoes CRUD e regras de negocio com validacoes
- Persistencia com SQLite
- Documentacao automatica com Swagger

## Autor

Gabriel Oliveira Alves

## Licenca

Projeto de estudo para fins educacionais.
