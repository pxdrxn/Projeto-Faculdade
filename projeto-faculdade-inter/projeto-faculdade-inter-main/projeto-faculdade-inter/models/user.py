from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from database import metadata

usuarios = Table(
    "usuarios",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False),
    Column("email", String, unique=True, nullable=False),
    Column("telefone", String, nullable=False),
    Column("password", String, nullable=False),
    Column("tipo_usuario", String, nullable=False)  # "cliente" ou "prestador"
)
