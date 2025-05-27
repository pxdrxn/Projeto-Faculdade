from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from schemas.problem import ProblemIn, ProblemOut
from database import database
from models.problemas import problemas
from models.user import usuarios
from models.assinatura import assinaturas
from auth.dependencies import get_current_user

router = APIRouter()

# Criação de problema: aqui, o cliente envia a descrição e o cliente_id
@router.post("/problemas", response_model=ProblemOut)
async def criar_problema(problema: ProblemIn, user: dict = Depends(get_current_user)):
    if user["tipo"] != "cliente":
        raise HTTPException(status_code=403, detail="Apenas clientes podem criar problemas")

    # Usar o ID do token, e não mais do corpo da requisição
    cliente_id = int(user["sub"])

    query = problemas.insert().values(
        tipo_de_aparelho=problema.tipo_de_aparelho,
        marca=problema.marca,
        descricao=problema.descricao,
        cliente_id=cliente_id
    )
    id_problema = await database.execute(query)

    return ProblemOut(
        id=id_problema,
        tipo_de_aparelho=problema.tipo_de_aparelho,
        marca=problema.marca,
        descricao=problema.descricao,
        cliente_id=cliente_id
    )


# Listar problemas: se o usuário for prestador sem assinatura, o 'cliente_id' é ocultado
@router.get("/problemas", response_model=List[ProblemOut])
async def listar_problemas(user: dict = Depends(get_current_user)):
    query = select(
        problemas.c.id,
        problemas.c.tipo_de_aparelho,
        problemas.c.marca,
        problemas.c.descricao,
        problemas.c.cliente_id,
        usuarios.c.telefone
    ).select_from(
        problemas.join(usuarios, problemas.c.cliente_id == usuarios.c.id)
    )

    rows = await database.fetch_all(query)

    tem_assinatura = False
    if user["tipo"] == "prestador":
        tem_assinatura = await assinatura_valida(int(user["sub"]))

    response = []
    for row in rows:
        problema_data = {
            "id": row["id"],
            "tipo_de_aparelho": row["tipo_de_aparelho"],
            "marca": row["marca"],
            "descricao": row["descricao"],
            "cliente_id": row["cliente_id"] if user["tipo"] == "cliente" or tem_assinatura else None,
            "cliente_telefone": row["telefone"] if user["tipo"] == "cliente" or tem_assinatura else None
        }
        response.append(ProblemOut(**problema_data))

    if not response:
        raise HTTPException(status_code=404, detail="Nenhum problema encontrado")

    return response

# Verifica se o prestador tem uma assinatura ativa (sem verificar data)
async def assinatura_valida(prestador_id: int):
    assinatura = await database.fetch_one(
        select(assinaturas).where(
            (assinaturas.c.prestador_id == prestador_id) &
            (assinaturas.c.ativa == True)
        )
    )
    return assinatura is not None
