from fastapi import APIRouter, Depends
from security import login_required
from schemas.banking import SaqueIn, TransactionIn, DepositIn
from views.banking import DepositOut, ExtratoOut, SaqueOut, TransactionOut
from services.banking import Banking
from models.transactions import transactions

router = APIRouter(prefix='/bank', dependencies=[Depends(login_required)], tags=['Banking'])

service = Banking()

@router.post('/deposit', response_model=DepositOut)
async def deposit_money(deposit_value: DepositIn, id=Depends(login_required)):
  query = await service.deposit(deposit_value, id)
  return query

@router.post('/transfer', response_model=TransactionOut)
async def transfer_money(id:TransactionIn, id_user=Depends(login_required)):
  query = await service.transfer(id, id_user)
  return query

@router.post('/withdraw', response_model=SaqueOut)
async def withdraw(withdraw_data: SaqueIn, user_data=Depends(login_required)):
  query = await service.withdraw(withdraw_data, user_data)
  return query


@router.get('/statement', response_model=list[ExtratoOut])
async def statement(id=Depends(login_required)):
  query = await service.get_statements(id)
  return query