from datetime import datetime, timedelta
from jose import JWTError, jwt

# Chave secreta para assinar o token
SECRET_KEY = "sport_maior_do_ne"  # Troque por uma mais segura
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60 * 24  # 24 horas

def criar_token(dados: dict):
    to_encode = dados.copy()
    expiracao = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    to_encode.update({"exp": expiracao})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
