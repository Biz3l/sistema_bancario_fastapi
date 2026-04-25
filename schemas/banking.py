from pydantic import BaseModel

class TransactionIn(BaseModel):
  value: int | float
  receiver_id: int

class ExtratoIn(BaseModel):
  user_id: int

class DepositIn(BaseModel):
  value: int | float

class SaqueIn(BaseModel):
  value: int | float