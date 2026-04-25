from pydantic import BaseModel

class TransactionOut(BaseModel):
  user_id: int
  user: str
  value: int | float
  balance: int | float
  created_at: str
  completed: bool

class ExtratoOut(BaseModel):
  user_id: int
  user: str
  type: str
  receiver_id: int | None = None
  value: int | float
  created_at: str

class DepositOut(BaseModel):
  success: bool
  value_deposited: int | float
  user_id: int

class SaqueOut(BaseModel):
  user_id: int
  user: str
  value: int | float
  new_balance: int | float
