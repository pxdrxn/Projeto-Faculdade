from fastapi import APIRouter, HTTPException, Depends
from schemas.assinatura import AssinaturaIn, AssinaturaOut
from database import database
from models.assinatura import assinaturas
from models.user import usuarios
from auth.dependencies import get_current_user

router = APIRouter(tags=["Assinaturas"])

@router.post("/assinaturas", response_model=AssinaturaOut)
async def criar_assinatura(user: dict = Depends(get_current_user)):
    if user["tipo"] != "prestador":
        raise HTTPException(status_code=403, detail="Apenas prestadores podem criar assinaturas")

    prestador_id = int(user["sub"])

    existing = await database.fetch_one(
        assinaturas.select().where(
            (assinaturas.c.prestador_id == prestador_id) &
            (assinaturas.c.ativa == True)
        )
    )
    if existing:
        raise HTTPException(status_code=400, detail="Prestador já possui assinatura ativa")

    query = assinaturas.insert().values(
        prestador_id=prestador_id,
        ativa=True
    )
    assinatura_id = await database.execute(query)

    return await database.fetch_one(assinaturas.select().where(assinaturas.c.id == assinatura_id))

