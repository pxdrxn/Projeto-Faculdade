from pydantic import BaseModel, ConfigDict

class AssinaturaIn(BaseModel):
    prestador_id: int  # ID do prestador que deseja assinar

class AssinaturaOut(BaseModel):
    id: int
    prestador_id: int
    ativa: bool

class Config:
    model_config = ConfigDict(from_attributes=True)

