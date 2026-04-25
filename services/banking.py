from schemas.banking import TransactionIn, DepositIn, SaqueIn
from fastapi import HTTPException, status
from models.transactions import transactions
from models.user import users
from database import database
from views.banking import TransactionOut, DepositOut, ExtratoOut, SaqueOut
from datetime import datetime

class Banking:
  async def transfer(self, id:TransactionIn, id_user):
    if id.receiver_id == id_user['user_id']:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user can't be yourself.")

    if not id.value > 0:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please insert a valid number.")
    
    try:
      querytransaction = transactions.insert().values(
        user_id=id_user['user_id'],
        value=-id.value,
        receiver_id=id.receiver_id,
        type='Transfer'
      )
      selectqueryuser = users.select().where(users.c.id==id_user['user_id'])
      user = await database.fetch_one(selectqueryuser)
    
      selectdestinationuser = users.select().where(users.c.id==id.receiver_id)
      receiver_user = await database.fetch_one(selectdestinationuser)

      if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
      if user['balance'] <= id.value:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insuficient Balance.")
      
      if receiver_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Destination user not found.")
      
      updatequeryuser = users.update().where(users.c.id==id_user['user_id']).values(balance=users.c.balance - id.value)
      await database.execute(updatequeryuser)  
      updatedestinationuser = users.update().where(users.c.id==id.receiver_id).values(balance=users.c.balance + id.value)
      await database.execute(updatedestinationuser)
      await database.execute(querytransaction)
      
      user = await database.fetch_one(selectqueryuser)

      return TransactionOut(
        user_id=id_user['user_id'],
        user=user['name'],
        value=id.value,
        balance=user['balance'],
        created_at=datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
        completed=True
      )
    
    except HTTPException:
      raise
    except Exception as e:
      print(e)
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
  async def deposit(self, deposit_value: DepositIn, id):
    if not deposit_value.value > 0:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please insert a valid number.")
    try:
      querytransaction = transactions.insert().values(
        user_id=id['user_id'], 
        value=deposit_value.value,
        type='Deposit'
      )
      queryuser = users.update().where(users.c.id==id['user_id']).values(balance=users.c.balance + deposit_value.value)
      queryselectuser = users.select().where(users.c.id==id['user_id'])
      
      await database.execute(querytransaction)
      await database.execute(queryuser)

      user = await database.fetch_one(queryselectuser)

      if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
      return DepositOut(
        success=True,
        value_deposited=deposit_value.value,
        user_id=id['user_id']
        )
    except HTTPException:
      raise
    except Exception:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
  
  async def get_statements(self, id: int):
    userquery = users.select().where(users.c.id == id['user_id'])
    user = await database.fetch_one(userquery)

    if user is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    statementquery = transactions.select().where(transactions.c.user_id == id['user_id'])
    transactionsresult = await database.fetch_all(statementquery)

    return [ExtratoOut(
      user_id=id['user_id'],
      user=user['name'],
      type=transaction['type'],
      receiver_id=transaction['receiver_id'] if transaction['receiver_id'] else None,
      value=transaction['value'],
      created_at=transaction['created_at'].strftime('%d-%m-%Y %H:%M:%S'),
    )
    for transaction in transactionsresult]
  
  async def withdraw(self, withdraw_data: SaqueIn, user_data):
    id = user_data['user_id']
    withdraw_value = withdraw_data.value

    if not withdraw_value > 0:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Value not valid.")
    
    query = users.select().where(users.c.id == id)
    user = await database.fetch_one(query)
    
    if user is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    if user['balance'] < withdraw_value:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insuficient balance.")
    
    update_user_balance_query = users.update().where(users.c.id==id).values(balance=users.c.balance - withdraw_value)
    update_user_balance = await database.execute(update_user_balance_query)

    user = await database.fetch_one(query)

    querytransaction = transactions.insert().values(
          user_id=id, 
          value=-withdraw_value,
          type='Withdraw',
        )
    add_transaction = await database.execute(querytransaction)

    return SaqueOut(
      user_id=user['id'],
      user=user['name'],
      value=withdraw_value,
      new_balance=user['balance']
  )