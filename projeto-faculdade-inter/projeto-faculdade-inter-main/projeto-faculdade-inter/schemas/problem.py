from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from sqlalchemy import select


class ProblemIn(BaseModel):
    tipo_de_aparelho: str
    marca: str
    descricao: str

class ProblemOut(BaseModel):
    id: int
    tipo_de_aparelho: str
    marca: str
    descricao: str
    cliente_id: Optional[int] = None  # Agora é opcional
    cliente_telefone: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)