from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.sql import func
from database import metadata

problemas = Table(
    "problemas",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("tipo_de_aparelho", String, nullable=False),
    Column("marca", String, nullable=False),
    Column("descricao", String, nullable=False),
    Column("cliente_id", Integer, ForeignKey("usuarios.id"), nullable=False),
)
