from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as usuarios_router
from routes.problemas import router as problemas_router
from routes.assinaturas import router as assinaturas_router
from database import database, metadata, engine
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer

app = FastAPI()

# Adiciona o middleware CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Permite que o frontend em http://127.0.0.1:5500 acesse o backend
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Adiciona suporte ao botão "Authorize" com JWT
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API de Usuários e Problemas",
        version="1.0.0",
        description="Autenticação com JWT",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Cria todas as tabelas definidas no metadata (incluindo usuários, problemas e assinaturas)
metadata.create_all(bind=engine)

# Evento de startup para conectar ao banco
@app.on_event("startup")
async def startup():
    await database.connect()

# Evento de shutdown para desconectar do banco
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Inclusão das rotas
app.include_router(usuarios_router)
app.include_router(problemas_router)
app.include_router(assinaturas_router)
