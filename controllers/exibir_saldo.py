from fastapi import APIRouter, status, HTTPException, Depends
from schemas.user import userBalanceIn
from database import database
from models.user import users
from security import login_required
from views.user import userBalanceOut

router = APIRouter(prefix='/balance', dependencies=[Depends(login_required)], tags=["Balance"])


@router.get('', response_model=userBalanceOut, description='Operação para checar saldo.')
async def get_balance(id = Depends(login_required)):
    query = users.select().where(users.c.id == id['user_id'])

    try:
      userBalance = await database.fetch_one(query) 
      return userBalanceOut(
      user=userBalance["name"],
      balance=userBalance["balance"]
      )
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found!")

    
  