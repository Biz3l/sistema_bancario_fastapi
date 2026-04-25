from pydantic import BaseModel

class userIn(BaseModel):
  name: str

class userBalanceIn(BaseModel):
  user_id: int
