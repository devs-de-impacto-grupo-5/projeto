#!/bin/bash

# Exemplo rápido de teste - Execute passo a passo

BASE_URL="http://localhost:8084"

echo "=========================================="
echo "  EXEMPLO RÁPIDO DE TESTE"
echo "=========================================="
echo ""

# PASSO 1: Criar Produtor 1
echo "1. Criando Produtor 1..."
curl -X 'POST' \
  "${BASE_URL}/register" \
  -H 'Content-Type: application/json' \
  -d '{
    "tipo_usuario": "produtor",
    "subtipo_usuario": "fornecedor_individual",
    "name": "João Silva",
    "email": "joao@example.com",
    "senha": "senha123",
    "cpf": "123.456.789-10"
}'
echo -e "\n"

# PASSO 2: Criar Produtor 2
echo "2. Criando Produtor 2..."
curl -X 'POST' \
  "${BASE_URL}/register" \
  -H 'Content-Type: application/json' \
  -d '{
    "tipo_usuario": "produtor",
    "subtipo_usuario": "grupo_formal",
    "name": "Associação ABC",
    "email": "assoc@example.com",
    "senha": "senha123",
    "cnpj": "12.345.678/0001-99"
}'
echo -e "\n"

# PASSO 3: Criar Entidade Executora
echo "3. Criando Entidade Executora..."
curl -X 'POST' \
  "${BASE_URL}/register" \
  -H 'Content-Type: application/json' \
  -d '{
    "tipo_usuario": "entidade_executora",
    "subtipo_usuario": "escola",
    "name": "Escola Estadual",
    "email": "escola@example.com",
    "senha": "senha123",
    "nome_escola": "Escola Estadual ABC"
}'
echo -e "\n"

# PASSO 4: Obter Token da Entidade
echo "4. Obtendo token da entidade..."
TOKEN=$(curl -s -X 'POST' \
  "${BASE_URL}/token" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=escola@example.com&password=senha123' | jq -r '.access_token')

echo "Token: ${TOKEN:0:30}..."
echo ""

# PASSO 5: Validar CPF
echo "5. Validando CPF..."
curl -X 'POST' \
  "${BASE_URL}/validar-usuario" \
  -H 'Content-Type: application/json' \
  -d '{"documento": "123.456.789-10"}'
echo -e "\n"

# PASSO 6: Criar Demanda
echo "6. Criando demanda relacionando produto 1 + produtor 1 e produto 3 + produtor 2..."
curl -X 'POST' \
  "${BASE_URL}/demandas" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H 'Content-Type: application/json' \
  -d '{
    "titulo": "Demanda de Alimentos - Janeiro 2025",
    "descricao": "Demanda de produtos alimentícios",
    "quantidade": 1500,
    "itens": [
      {
        "produto_id": 1,
        "user_id": 1,
        "unidade_id": 1,
        "quantidade": "1000.00",
        "preco_maximo": "5.50",
        "observacoes": "Arroz tipo 1"
      },
      {
        "produto_id": 3,
        "user_id": 2,
        "unidade_id": 1,
        "quantidade": "500.00",
        "preco_maximo": "8.00",
        "observacoes": "Tomate vermelho"
      }
    ],
    "encerra_em": "2025-01-15T23:59:59"
  }'
echo -e "\n"

echo "=========================================="
echo "  TESTE CONCLUÍDO!"
echo "=========================================="

