from fastapi import APIRouter, HTTPException, Depends
from schemas.user import UserCreate, UserLogin
from database import database
from models.user import usuarios
from auth.jwt_handler import criar_token
from auth.dependencies import get_current_user

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate):
    if user.tipo_usuario not in ["cliente", "prestador"]:
        raise HTTPException(status_code=400, detail="Tipo de usuário inválido. Escolha entre 'cliente' ou 'prestador'.")
    
    
    verificar_query = usuarios.select().where(usuarios.c.email == user.email)
    existente = await database.fetch_one(verificar_query)
    if existente:
        raise HTTPException(status_code=409, detail="Usuário já existente.")
    
    query = usuarios.insert().values(
        username=user.username,
        email=user.email,
        password=user.password,  
        telefone=user.telefone, 
        tipo_usuario=user.tipo_usuario,
    )
    
    await database.execute(query)
    return {"mensagem": "Usuário criado com sucesso!"}

@router.post("/login")
async def login(user: UserLogin):
    query = usuarios.select().where(
        (usuarios.c.email == user.email) & (usuarios.c.password == user.password)
    )
    resultado = await database.fetch_one(query)
    if resultado is None:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos.")
    
    token = criar_token({"sub": str(resultado["id"]), "tipo": resultado["tipo_usuario"]})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/usuarios")
async def listar_users():
    query = usuarios.select()
    resultado = await database.fetch_all(query)
    return resultado

@router.get("/rota_protegida")
async def rota_protegida(usuario = Depends(get_current_user)):
    return {"msg": f"Você está autenticado! ID: {usuario['sub']} - Tipo: {usuario['tipo']}"}
