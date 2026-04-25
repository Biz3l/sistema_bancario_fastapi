from pydantic import BaseModel


class userOut(BaseModel):
  user_id: int | None = None
  name: str
  balance: int | float
  

class userBalanceOut(BaseModel):
  user: str
  balance: int | float