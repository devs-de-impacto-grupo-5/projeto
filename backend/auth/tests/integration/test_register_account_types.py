import pytest
from fastapi.testclient import TestClient
from main import app
import time

# Testes de integração para os diferentes tipos de conta

def test_registrar_fornecedor_individual():
    """Testa o registro de fornecedor individual"""
    client = TestClient(app)
    unique_email = f"fornecedor_{int(time.time())}@example.com"

    payload = {
        "tipo_conta": "fornecedor_individual",
        "name": "João Silva",
        "email": unique_email,
        "senha": "senha_segura_123",
        "cpf": "123.456.789-10"
    }

    response = client.post("/register", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 201
    data = response.json()
    assert "user_id" in data
    assert data["tipo_conta"] == "fornecedor_individual"
    assert data["message"] == "Conta fornecedor_individual criada com sucesso"


def test_registrar_grupo_informal():
    """Testa o registro de grupo informal"""
    client = TestClient(app)
    unique_email = f"grupo_inf_{int(time.time())}@example.com"

    payload = {
        "tipo_conta": "grupo_informal",
        "name": "Grupo Informal de Produtores",
        "email": unique_email,
        "senha": "senha_segura_123",
        "cpfs": ["123.456.789-10", "234.567.890-21", "345.678.901-32"]
    }

    response = client.post("/register", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 201
    data = response.json()
    assert "user_id" in data
    assert data["tipo_conta"] == "grupo_informal"
    assert data["message"] == "Conta grupo_informal criada com sucesso"


def test_registrar_grupo_formal():
    """Testa o registro de grupo formal"""
    client = TestClient(app)
    unique_email = f"grupo_formal_{int(time.time())}@example.com"

    payload = {
        "tipo_conta": "grupo_formal",
        "name": "Associação de Produtores",
        "email": unique_email,
        "senha": "senha_segura_123",
        "cnpj": "12.345.678/0001-99"
    }

    response = client.post("/register", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 201
    data = response.json()
    assert "user_id" in data
    assert data["tipo_conta"] == "grupo_formal"
    assert data["message"] == "Conta grupo_formal criada com sucesso"


def test_registrar_email_duplicado():
    """Testa se impede registro com email duplicado"""
    client = TestClient(app)
    email_duplicado = f"duplicado_{int(time.time())}@example.com"

    # Primeiro registro
    payload1 = {
        "tipo_conta": "fornecedor_individual",
        "name": "Primeiro Registro",
        "email": email_duplicado,
        "senha": "senha_segura_123",
        "cpf": "111.111.111-11"
    }
    response1 = client.post("/register", json=payload1)
    assert response1.status_code == 201

    # Segundo registro com mesmo email
    payload2 = {
        "tipo_conta": "fornecedor_individual",
        "name": "Segundo Registro",
        "email": email_duplicado,
        "senha": "senha_segura_456",
        "cpf": "222.222.222-22"
    }
    response2 = client.post("/register", json=payload2)
    assert response2.status_code == 400
    assert "Email já cadastrado" in response2.json()["detail"]


def test_registrar_cpf_duplicado():
    """Testa se impede registro com CPF duplicado"""
    client = TestClient(app)
    cpf_duplicado = "333.333.333-33"

    # Primeiro registro
    payload1 = {
        "tipo_conta": "fornecedor_individual",
        "name": "Primeiro CPF",
        "email": f"cpf_dup_1_{int(time.time())}@example.com",
        "senha": "senha_segura_123",
        "cpf": cpf_duplicado
    }
    response1 = client.post("/register", json=payload1)
    assert response1.status_code == 201

    # Segundo registro com mesmo CPF
    payload2 = {
        "tipo_conta": "fornecedor_individual",
        "name": "Segundo CPF",
        "email": f"cpf_dup_2_{int(time.time())}@example.com",
        "senha": "senha_segura_456",
        "cpf": cpf_duplicado
    }
    response2 = client.post("/register", json=payload2)
    assert response2.status_code == 400
    assert "CPF já cadastrado" in response2.json()["detail"]


def test_registrar_sem_cpf_obrigatorio():
    """Testa se valida CPF obrigatório para fornecedor individual"""
    client = TestClient(app)

    payload = {
        "tipo_conta": "fornecedor_individual",
        "name": "Sem CPF",
        "email": f"sem_cpf_{int(time.time())}@example.com",
        "senha": "senha_segura_123"
    }

    response = client.post("/register", json=payload)
    assert response.status_code == 422
    assert "CPF é obrigatório" in response.json()["detail"]


def test_registrar_tipo_conta_invalido():
    """Testa se valida tipo de conta inválido"""
    client = TestClient(app)

    payload = {
        "tipo_conta": "tipo_invalido",
        "name": "Tipo Inválido",
        "email": f"tipo_inv_{int(time.time())}@example.com",
        "senha": "senha_segura_123",
        "cpf": "444.444.444-44"
    }

    response = client.post("/register", json=payload)
    assert response.status_code == 422
