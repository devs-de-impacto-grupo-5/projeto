#!/bin/bash

# Script completo de teste da aplicação
# Executa todo o fluxo desde criação de usuários até criação de demandas

BASE_URL="http://localhost:8084"

echo "=========================================="
echo "  TESTE COMPLETO DA APLICAÇÃO"
echo "=========================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para fazer requisições e mostrar resultado
make_request() {
    local method=$1
    local endpoint=$2
    local data=$3
    local token=$4
    local description=$5
    
    echo -e "${BLUE}→ ${description}${NC}"
    
    if [ -n "$token" ]; then
        response=$(curl -s -X "$method" \
            "${BASE_URL}${endpoint}" \
            -H "Authorization: Bearer ${token}" \
            -H 'Content-Type: application/json' \
            -d "$data")
    else
        if [ "$method" = "POST" ] && [ -n "$data" ]; then
            response=$(curl -s -X "$method" \
                "${BASE_URL}${endpoint}" \
                -H 'Content-Type: application/json' \
                -d "$data")
        else
            response=$(curl -s -X "$method" \
                "${BASE_URL}${endpoint}" \
                -H 'Content-Type: application/x-www-form-urlencoded' \
                -d "$data")
        fi
    fi
    
    echo "$response" | jq '.' 2>/dev/null || echo "$response"
    echo ""
    
    echo "$response"
}

echo -e "${GREEN}=== PASSO 1: Criando Usuários ===${NC}"
echo ""

# 1. Criar Produtor 1
echo -e "${YELLOW}1.1. Criando Produtor Individual...${NC}"
PRODUTOR1=$(make_request "POST" "/register" '{
    "tipo_usuario": "produtor",
    "subtipo_usuario": "fornecedor_individual",
    "name": "João Silva",
    "email": "joao.silva@example.com",
    "senha": "senha123",
    "cpf": "123.456.789-10"
}' "" "Criando Produtor 1 (Fornecedor Individual)")

PRODUTOR1_ID=$(echo "$PRODUTOR1" | jq -r '.user_id // empty')
if [ -z "$PRODUTOR1_ID" ]; then
    echo "Erro ao criar Produtor 1. Verifique se o email já existe."
    exit 1
fi
echo -e "${GREEN}✓ Produtor 1 criado com ID: ${PRODUTOR1_ID}${NC}"
echo ""

# 2. Criar Produtor 2
echo -e "${YELLOW}1.2. Criando Produtor Grupo Formal...${NC}"
PRODUTOR2=$(make_request "POST" "/register" '{
    "tipo_usuario": "produtor",
    "subtipo_usuario": "grupo_formal",
    "name": "Associação de Produtores ABC",
    "email": "assoc.abc@example.com",
    "senha": "senha123",
    "cnpj": "12.345.678/0001-99"
}' "" "Criando Produtor 2 (Grupo Formal)")

PRODUTOR2_ID=$(echo "$PRODUTOR2" | jq -r '.user_id // empty')
if [ -z "$PRODUTOR2_ID" ]; then
    echo "Erro ao criar Produtor 2. Verifique se o email já existe."
    exit 1
fi
echo -e "${GREEN}✓ Produtor 2 criado com ID: ${PRODUTOR2_ID}${NC}"
echo ""

# 3. Criar Entidade Executora
echo -e "${YELLOW}1.3. Criando Entidade Executora (Escola)...${NC}"
ENTIDADE=$(make_request "POST" "/register" '{
    "tipo_usuario": "entidade_executora",
    "subtipo_usuario": "escola",
    "name": "Escola Estadual Exemplo",
    "email": "escola@example.com",
    "senha": "senha123",
    "nome_escola": "Escola Estadual ABC",
    "endereco": "Rua das Escolas, 123",
    "telefone": "(21) 3333-4444"
}' "" "Criando Entidade Executora")

ENTIDADE_ID=$(echo "$ENTIDADE" | jq -r '.user_id // empty')
if [ -z "$ENTIDADE_ID" ]; then
    echo "Erro ao criar Entidade Executora. Verifique se o email já existe."
    exit 1
fi
echo -e "${GREEN}✓ Entidade Executora criada com ID: ${ENTIDADE_ID}${NC}"
echo ""

echo -e "${GREEN}=== PASSO 2: Obtendo Tokens de Autenticação ===${NC}"
echo ""

# Login Entidade
echo -e "${YELLOW}2.1. Fazendo login da Entidade Executora...${NC}"
TOKEN_ENTIDADE_RESPONSE=$(curl -s -X 'POST' \
    "${BASE_URL}/token" \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'username=escola@example.com&password=senha123')

TOKEN_ENTIDADE=$(echo "$TOKEN_ENTIDADE_RESPONSE" | jq -r '.access_token // empty')
if [ -z "$TOKEN_ENTIDADE" ] || [ "$TOKEN_ENTIDADE" = "null" ]; then
    echo "Erro ao obter token da entidade"
    echo "$TOKEN_ENTIDADE_RESPONSE"
    exit 1
fi
echo -e "${GREEN}✓ Token obtido: ${TOKEN_ENTIDADE:0:30}...${NC}"
echo ""

echo -e "${GREEN}=== PASSO 3: Validando Documentos ===${NC}"
echo ""

# Validar CPF não cadastrado
echo -e "${YELLOW}3.1. Validando CPF não cadastrado...${NC}"
make_request "POST" "/validar-usuario" '{"documento": "999.888.777-66"}' "" "Validando CPF não cadastrado"

# Validar CPF cadastrado
echo -e "${YELLOW}3.2. Validando CPF já cadastrado...${NC}"
make_request "POST" "/validar-usuario" '{"documento": "123.456.789-10"}' "" "Validando CPF cadastrado"

# Validar CNPJ
echo -e "${YELLOW}3.3. Validando CNPJ...${NC}"
make_request "POST" "/validar-usuario" '{"documento": "12.345.678/0001-99"}' "" "Validando CNPJ"

echo -e "${GREEN}=== PASSO 4: Verificando Catálogo ===${NC}"
echo ""

echo -e "${YELLOW}4.1. Verificando produtos no catálogo...${NC}"
PRODUTOS=$(docker exec rj_devs_postgres psql -U rj_devs_user -d rj_devs_auth -t -c "SELECT id, nome FROM catalogo_produtos LIMIT 5;" 2>/dev/null)
if [ -z "$PRODUTOS" ]; then
    echo "⚠️  Nenhum produto encontrado no catálogo. Você precisa criar produtos primeiro."
    echo "   Exemplo de SQL para criar produtos:"
    echo "   INSERT INTO unidades (codigo, nome, tipo) VALUES ('kg', 'Quilograma', 'mass');"
    echo "   INSERT INTO catalogo_produtos (nome, categoria, unidade_padrao_id) VALUES ('Arroz', 'graos', 1);"
else
    echo "$PRODUTOS"
fi
echo ""

echo -e "${YELLOW}4.2. Verificando unidades...${NC}"
UNIDADES=$(docker exec rj_devs_postgres psql -U rj_devs_user -d rj_devs_auth -t -c "SELECT id, codigo, nome FROM unidades LIMIT 5;" 2>/dev/null)
if [ -z "$UNIDADES" ]; then
    echo "⚠️  Nenhuma unidade encontrada. Você precisa criar unidades primeiro."
else
    echo "$UNIDADES"
fi
echo ""

# Obter IDs de exemplo (assumindo que existem)
PRODUTO_ID_1=1
PRODUTO_ID_2=3
UNIDADE_ID=1

echo -e "${GREEN}=== PASSO 5: Criando Demanda ===${NC}"
echo ""

echo -e "${YELLOW}5.1. Criando demanda relacionando múltiplos produtos e produtores...${NC}"
DEMANDA_DATA=$(cat <<EOF
{
    "titulo": "Demanda de Alimentos para Merenda Escolar - Janeiro 2025",
    "descricao": "Demanda de produtos alimentícios para merenda escolar do mês de janeiro",
    "quantidade": 1500,
    "itens": [
        {
            "produto_id": ${PRODUTO_ID_1},
            "user_id": ${PRODUTOR1_ID},
            "unidade_id": ${UNIDADE_ID},
            "quantidade": "1000.00",
            "preco_maximo": "5.50",
            "observacoes": "Arroz tipo 1, preferencialmente orgânico"
        },
        {
            "produto_id": ${PRODUTO_ID_2},
            "user_id": ${PRODUTOR2_ID},
            "unidade_id": ${UNIDADE_ID},
            "quantidade": "500.00",
            "preco_maximo": "8.00",
            "observacoes": "Tomate vermelho de boa qualidade"
        }
    ],
    "encerra_em": "2025-01-15T23:59:59",
    "local_entrega": {
        "endereco": "Rua das Escolas, 123",
        "cidade": "Rio de Janeiro",
        "uf": "RJ",
        "cep": "20000-000"
    }
}
EOF
)

DEMANDA_RESPONSE=$(make_request "POST" "/demandas" "$DEMANDA_DATA" "$TOKEN_ENTIDADE" "Criando Demanda")

DEMANDA_ID=$(echo "$DEMANDA_RESPONSE" | jq -r '.id // empty')
if [ -z "$DEMANDA_ID" ] || [ "$DEMANDA_ID" = "null" ]; then
    echo "Erro ao criar demanda"
    exit 1
fi
echo -e "${GREEN}✓ Demanda criada com ID: ${DEMANDA_ID}${NC}"
echo ""

echo -e "${GREEN}=== PASSO 6: Listando Demandas ===${NC}"
echo ""
make_request "GET" "/demandas" "" "$TOKEN_ENTIDADE" "Listando todas as demandas"

echo -e "${GREEN}=== PASSO 7: Obtendo Demanda Específica ===${NC}"
echo ""
make_request "GET" "/demandas/${DEMANDA_ID}" "" "$TOKEN_ENTIDADE" "Obtendo detalhes da demanda ${DEMANDA_ID}"

echo -e "${GREEN}=== PASSO 8: Listando Produtores que Podem Suprir ===${NC}"
echo ""
make_request "GET" "/demandas/${DEMANDA_ID}/produtores" "" "$TOKEN_ENTIDADE" "Listando produtores que podem suprir a demanda ${DEMANDA_ID}"

echo ""
echo -e "${GREEN}=========================================="
echo "  TESTE COMPLETO FINALIZADO COM SUCESSO!"
echo "==========================================${NC}"
echo ""
echo "Resumo:"
echo "  - Produtor 1 (ID: ${PRODUTOR1_ID}): João Silva"
echo "  - Produtor 2 (ID: ${PRODUTOR2_ID}): Associação ABC"
echo "  - Entidade (ID: ${ENTIDADE_ID}): Escola Estadual"
echo "  - Demanda (ID: ${DEMANDA_ID}): Criada com sucesso"
echo ""
echo "A demanda relaciona:"
echo "  - Produto ${PRODUTO_ID_1} → Produtor ${PRODUTOR1_ID} (quantidade: 1000)"
echo "  - Produto ${PRODUTO_ID_2} → Produtor ${PRODUTOR2_ID} (quantidade: 500)"
echo ""

