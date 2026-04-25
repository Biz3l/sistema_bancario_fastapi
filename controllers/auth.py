from fastapi import APIRouter
from schemas.auth import loginIn
from security import sign_jwt
from views.auth import loginOut

router = APIRouter(prefix=('/auth'), tags=['Auth'])

@router.post('/login', response_model=loginOut)
async def get_Login(data: loginIn):
  return sign_jwt(user_id=data.user_id)