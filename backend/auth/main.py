from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import uvicorn
from routers import (
    Login_routers,
    Produtos_routers,
    Editais_routers,
    Match_routers,
    Demanda_routers,
    Propostas_routers,
    Documentos_routers,
    Produtores_routers,
    Governo_routers,
    Contratos_routers,
    Admin_routers,
    Notificacoes_routers
)
from fastapi.security import HTTPBearer
from db.db import create_tables, get_db
from services.seed_catalog import seed_catalogo
from contextlib import asynccontextmanager
from dotenv import load_dotenv


# Load environment variables from .env before importing modules that rely on them
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables...")
    create_tables()
    print("Tables created.")
    # Seed catalog on startup
    try:
        db = next(get_db())
        seed_catalogo(db)
        db.close()
        print("Catalog seeded.")
    except Exception as e:
        print(f"Warning: Could not seed catalog: {e}")
    yield

# Criar uma instância do aplicativo FastAPI
app = FastAPI(title="Autenticador", version="1.0.0", root_path="/api/auth", lifespan=lifespan)

# Configuração do esquema de segurança para o Swagger
security_scheme = HTTPBearer(
    bearerFormat="JWT",
    scheme_name="Bearer"
)

# Função para personalizar a documentação OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="Autenticador de usuários",
        routes=app.routes,
    )
    
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}

    # Adiciona o esquema de segurança corretamente
    openapi_schema["components"]["securitySchemes"]["Bearer"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }

    # Aplica a segurança globalmente
    openapi_schema["security"] = [{"Bearer": []}]
    
    app.openapi_schema = openapi_schema
    return openapi_schema


# Aplica o esquema personalizado
app.openapi = custom_openapi

# Middleware de CORS - Permite qualquer origem
# Usa função para permitir qualquer origem mesmo com allow_credentials=True
def allow_all_origins(origin: str) -> bool:
    """Permite qualquer origem para evitar erros de CORS"""
    return True

app.add_middleware(
    CORSMiddleware,
    allow_origin_func=allow_all_origins,  # Permite qualquer origem via função
    allow_credentials=True,  # Permite credenciais (cookies, headers de auth)
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

# Incluir todos os routers
app.include_router(Login_routers)
app.include_router(Produtos_routers)
app.include_router(Editais_routers)
app.include_router(Match_routers)
app.include_router(Demanda_routers)
app.include_router(Propostas_routers)
app.include_router(Documentos_routers)
app.include_router(Produtores_routers)
app.include_router(Governo_routers)
app.include_router(Contratos_routers)
app.include_router(Admin_routers)
app.include_router(Notificacoes_routers)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8084, log_level="info")
