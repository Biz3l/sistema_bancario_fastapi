from contextlib import asynccontextmanager
from fastapi import FastAPI
from controllers import exibir_saldo, users, auth, bank
from database import database, metadata, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
  from models.user import users
  from models.transactions import transactions
  await database.connect()
  metadata.create_all(engine)
  yield
  await database.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(exibir_saldo.router)
app.include_router(auth.router)
app.include_router(bank.router)