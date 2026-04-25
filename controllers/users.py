from fastapi import APIRouter, HTTPException, status
from database import database
from schemas.user import userIn
from views.user import userOut
from models.user import users

router = APIRouter(prefix='/user')

@router.get("/", response_model=list[userOut])
async def get_users():
  query = users.select()
  rows = await database.fetch_all(query)
  return [userOut(user_id=row["id"],
                  name=row["name"],
                  balance=row["balance"]
                  )
                  for row in rows]
  

@router.post('/createuser', response_model=userOut, status_code=status.HTTP_201_CREATED)
async def create_users(user: userIn): 
  command = users.insert().values(
    name=user.name,
    balance=0,
    )
  
  try:
    user_id = await database.execute(command)
  except:
    raise HTTPException(
      status_code=409,
      detail="User already exists"
    )

  return {
          "name": user.name,
          "balance": 0,
          "user_id": user_id
          }
