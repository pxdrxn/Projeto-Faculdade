from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from auth.jwt_handler import verificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")  # mesma rota de login

async def get_current_user(token: str = Depends(oauth2_scheme)):
    dados = verificar_token(token)
    if not dados:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    return dados
