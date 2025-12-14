import pytest
from fastapi.testclient import TestClient
from main import app
import time

# Testes de integração para endpoints de produtos


@pytest.fixture
def usuario_autenticado():
    """Fixture que cria um usuário e retorna o token de autenticação"""
    client = TestClient(app)

    # Registra um usuário
    email = f"usuario_produtos_{int(time.time())}@example.com"
    payload_register = {
        "tipo_conta": "fornecedor_individual",
        "name": "Fornecedor Teste",
        "email": email,
        "senha": "senha_segura_123",
        "cpf": "123.456.789-10"
    }

    response = client.post("/register", json=payload_register)
    assert response.status_code == 201

    # Faz login para obter o token
    login_payload = {
        "username": email,
        "password": "senha_segura_123"
    }

    response = client.post("/token", data=login_payload)
    assert response.status_code == 200

    token = response.json()["access_token"]
    return client, token, email


def test_criar_produto(usuario_autenticado):
    """Testa a criação de um produto"""
    client, token, email = usuario_autenticado

    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "nome": "Maçã Gala",
        "descricao": "Maçã gala de primeira qualidade",
        "categoria": "Frutas",
        "quantidade": 100,
        "preco": 5.50
    }

    response = client.post("/produtos", json=payload, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Maçã Gala"
    assert data["quantidade"] == 100
    assert data["preco"] == 5.50
    assert "id" in data


def test_listar_produtos(usuario_autenticado):
    """Testa a listagem de produtos do usuário"""
    client, token, email = usuario_autenticado

    headers = {"Authorization": f"Bearer {token}"}

    # Cria alguns produtos
    produtos = [
        {
            "nome": "Maçã",
            "descricao": "Maçã vermelha",
            "categoria": "Frutas",
            "quantidade": 50,
            "preco": 4.00
        },
        {
            "nome": "Pera",
            "descricao": "Pera doce",
            "categoria": "Frutas",
            "quantidade": 30,
            "preco": 6.00
        }
    ]

    for produto in produtos:
        response = client.post("/produtos", json=produto, headers=headers)
        assert response.status_code == 201

    # Lista os produtos
    response = client.get("/produtos", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["produtos"]) == 2


def test_obter_produto(usuario_autenticado):
    """Testa a obtenção de um produto específico"""
    client, token, email = usuario_autenticado

    headers = {"Authorization": f"Bearer {token}"}

    # Cria um produto
    payload = {
        "nome": "Cenoura",
        "descricao": "Cenoura fresca",
        "categoria": "Vegetais",
        "quantidade": 200,
        "preco": 2.50
    }

    response = client.post("/produtos", json=payload, headers=headers)
    assert response.status_code == 201
    produto_id = response.json()["id"]

    # Obtém o produto
    response = client.get(f"/produtos/{produto_id}", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == produto_id
    assert data["nome"] == "Cenoura"


def test_atualizar_produto(usuario_autenticado):
    """Testa a atualização de um produto"""
    client, token, email = usuario_autenticado

    headers = {"Authorization": f"Bearer {token}"}

    # Cria um produto
    payload = {
        "nome": "Batata",
        "descricao": "Batata branca",
        "categoria": "Tubérculos",
        "quantidade": 500,
        "preco": 3.00
    }

    response = client.post("/produtos", json=payload, headers=headers)
    assert response.status_code == 201
    produto_id = response.json()["id"]

    # Atualiza o produto
    update_payload = {
        "quantidade": 400,
        "preco": 3.50
    }

    response = client.put(f"/produtos/{produto_id}", json=update_payload, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert data["quantidade"] == 400
    assert data["preco"] == 3.50
    assert data["nome"] == "Batata"  # Não foi alterado


def test_deletar_produto(usuario_autenticado):
    """Testa a deleção de um produto"""
    client, token, email = usuario_autenticado

    headers = {"Authorization": f"Bearer {token}"}

    # Cria um produto
    payload = {
        "nome": "Tomate",
        "descricao": "Tomate maduro",
        "categoria": "Vegetais",
        "quantidade": 150,
        "preco": 4.50
    }

    response = client.post("/produtos", json=payload, headers=headers)
    assert response.status_code == 201
    produto_id = response.json()["id"]

    # Deleta o produto
    response = client.delete(f"/produtos/{produto_id}", headers=headers)
    print(f"Status: {response.status_code}")

    assert response.status_code == 204

    # Verifica que o produto foi deletado
    response = client.get(f"/produtos/{produto_id}", headers=headers)
    assert response.status_code == 404


def test_criar_produto_sem_autenticacao():
    """Testa se a criação sem autenticação é bloqueada"""
    client = TestClient(app)

    payload = {
        "nome": "Produto Sem Auth",
        "descricao": "Teste",
        "categoria": "Teste",
        "quantidade": 10,
        "preco": 5.00
    }

    response = client.post("/produtos", json=payload)
    print(f"Status: {response.status_code}")

    assert response.status_code == 403  # Forbidden (sem token)


def test_produto_isolado_por_usuario(usuario_autenticado):
    """Testa que produtos de um usuário não são acessíveis por outro"""
    client, token1, email1 = usuario_autenticado

    headers1 = {"Authorization": f"Bearer {token1}"}

    # Primeiro usuário cria um produto
    payload = {
        "nome": "Produto User1",
        "descricao": "Teste",
        "categoria": "Teste",
        "quantidade": 10,
        "preco": 5.00
    }

    response = client.post("/produtos", json=payload, headers=headers1)
    assert response.status_code == 201
    produto_id = response.json()["id"]

    # Segundo usuário tenta acessar o produto do primeiro
    client2, token2, email2 = usuario_autenticado
    headers2 = {"Authorization": f"Bearer {token2}"}

    response = client2.get(f"/produtos/{produto_id}", headers=headers2)
    print(f"Status: {response.status_code}")

    assert response.status_code == 404  # Produto não encontrado para esse usuário
