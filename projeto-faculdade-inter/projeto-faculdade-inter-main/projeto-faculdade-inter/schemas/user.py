from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, Literal

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    telefone: int
    tipo_usuario: Literal["cliente", "prestador"]  # Ex.: "cliente" ou "prestador"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    tipo_usuario: str
    telefone: Optional[str] = None  # <-- Campo condicional

    model_config = ConfigDict(from_attributes=True)
