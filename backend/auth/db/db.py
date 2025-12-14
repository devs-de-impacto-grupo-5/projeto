# db/db.py
import importlib
import os
import pkgutil
from pathlib import Path
from threading import Lock

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.base import Base  # Importação correta da Base

load_dotenv()

engine = None
SessionLocal = None
_db_lock = Lock()

def get_engine():
    global engine
    # Double-checked locking to ensure thread safety
    if engine is None:
        with _db_lock:
            if engine is None:
                sqlalchemy_database_url = _get_database_url()
                engine = create_engine(sqlalchemy_database_url, echo=False) # Turned off echo for cleaner test output
    return engine

def get_session_local():
    global SessionLocal
    if SessionLocal is None:
        with _db_lock:
            if SessionLocal is None:
                SessionLocal = sessionmaker(bind=get_engine(), autocommit=False, autoflush=False)
    return SessionLocal


def get_db():
    # This function is overridden in tests, but kept for the main app
    Session = get_session_local()
    db = Session()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Importa os modelos APÓS criar a Base"""
    _import_all_models()

    db_engine = get_engine()
    Base.metadata.create_all(bind=db_engine)

def drop_tables():
    _import_all_models()
    db_engine = get_engine()
    Base.metadata.drop_all(bind=db_engine)

def _get_database_url() -> str:
    """
    Monta a URL de conexão.
    Prioriza DATABASE_URL e, se ausente, tenta montar a partir das variáveis POSTGRES_* (compatível com docker-compose/.env).
    """
    url = os.getenv("DATABASE_URL")
    if url:
        return url

    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DB")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")

    if user and password and db_name:
        return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

    raise ValueError("DATABASE_URL não está definida e as variáveis POSTGRES_* não foram informadas.")


def _import_all_models():
    """
    Carrega todos os módulos em models/ dinamicamente para garantir que Base.metadata conheça todas as tabelas.
    Evita ter que manter uma lista manual em create_tables().
    """
    package_name = "models"
    models_pkg = importlib.import_module(package_name)
    package_path = Path(models_pkg.__file__).parent

    for module in pkgutil.iter_modules([str(package_path)]):
        if module.ispkg or module.name.startswith("__"):
            continue
        importlib.import_module(f"{package_name}.{module.name}")

# Chame create_tables() apenas se executado diretamente
if __name__ == "__main__":
    create_tables()
