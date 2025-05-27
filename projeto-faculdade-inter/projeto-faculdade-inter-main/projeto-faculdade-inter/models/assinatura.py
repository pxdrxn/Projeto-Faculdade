from sqlalchemy import Table, Column, Integer, Boolean, ForeignKey
from sqlalchemy.sql import func
from database import metadata

assinaturas = Table(
    "assinaturas",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("prestador_id", Integer, ForeignKey("usuarios.id"), nullable=False),
    Column("ativa", Boolean, default=True),
)