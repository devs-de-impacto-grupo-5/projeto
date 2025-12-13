"""
Testes integrados para o sistema de criação automática de documentos pendentes
para produtores no registro.
"""
import json
import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from main import app
from db.db import get_db
from models.User_model import User
from models.Documentos_model import DocumentoUsuario


@pytest.fixture
async def client():
    """Cria cliente HTTP para testes"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_fornecedor_individual_cria_8_documentos(client):
    """Testa se fornecedor_individual cria 8 documentos pendentes"""
    response = await client.post(
        "/api/auth/register",
        json={
            "tipo_usuario": "produtor",
            "subtipo_usuario": "fornecedor_individual",
            "name": "João Agricola",
            "email": "joao.agricola@test.com",
            "senha": "senha123",
            "cpf": "123.456.789-01"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["documentos_pendentes"] == 8
    assert data["tipo_usuario"] == "produtor"
    assert data["subtipo_usuario"] == "fornecedor_individual"


@pytest.mark.asyncio
async def test_grupo_informal_cria_8_documentos(client):
    """Testa se grupo_informal cria 8 documentos pendentes"""
    response = await client.post(
        "/api/auth/register",
        json={
            "tipo_usuario": "produtor",
            "subtipo_usuario": "grupo_informal",
            "name": "Grupo de Produtores",
            "email": "grupo@test.com",
            "senha": "senha123",
            "participantes": [
                {"nome": "Joao Silva", "cpf": "111.111.111-11"},
                {"nome": "Maria Santos", "cpf": "222.222.222-22"}
            ]
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["documentos_pendentes"] == 8
    assert data["tipo_usuario"] == "produtor"
    assert data["subtipo_usuario"] == "grupo_informal"


@pytest.mark.asyncio
async def test_grupo_formal_cria_11_documentos(client):
    """Testa se grupo_formal cria 11 documentos pendentes"""
    response = await client.post(
        "/api/auth/register",
        json={
            "tipo_usuario": "produtor",
            "subtipo_usuario": "grupo_formal",
            "name": "Associação de Produtores",
            "email": "assoc@test.com",
            "senha": "senha123",
            "cnpj": "12.345.678/0001-90"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["documentos_pendentes"] == 11
    assert data["tipo_usuario"] == "produtor"
    assert data["subtipo_usuario"] == "grupo_formal"


@pytest.mark.asyncio
async def test_entidade_executora_escola_nao_cria_documentos(client):
    """Testa que entidade_executora (escola) não cria documentos"""
    response = await client.post(
        "/api/auth/register",
        json={
            "tipo_usuario": "entidade_executora",
            "subtipo_usuario": "escola",
            "name": "Escola Pública",
            "email": "escola@test.com",
            "senha": "senha123",
            "nome_escola": "Escola Estadual XYZ"
        }
    )

    assert response.status_code == 201
    data = response.json()
    # Entidades executoras não devem ter documentos pendentes
    assert "documentos_pendentes" not in data
    assert data["tipo_usuario"] == "entidade_executora"


@pytest.mark.asyncio
async def test_entidade_executora_governo_nao_cria_documentos(client):
    """Testa que entidade_executora (governo) não cria documentos"""
    response = await client.post(
        "/api/auth/register",
        json={
            "tipo_usuario": "entidade_executora",
            "subtipo_usuario": "governo",
            "name": "Secretaria Municipal",
            "email": "govmun@test.com",
            "senha": "senha123",
            "nome_orgao": "Secretaria de Agricultura",
            "nivel": "municipal"
        }
    )

    assert response.status_code == 201
    data = response.json()
    # Entidades executoras não devem ter documentos pendentes
    assert "documentos_pendentes" not in data
    assert data["tipo_usuario"] == "entidade_executora"
