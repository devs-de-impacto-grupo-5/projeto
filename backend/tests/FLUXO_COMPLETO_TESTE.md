# Fluxo Completo de Teste da Aplicação

Este documento fornece um guia passo a passo para testar toda a aplicação, desde o cadastro de usuários até a criação de demandas relacionando produtos e produtores.

## Pré-requisitos

- Servidor rodando em `http://localhost:8084`
- Banco de dados PostgreSQL configurado e rodando
- Docker Compose executando (se aplicável)

## Passo 1: Criar Usuários

### 1.1. Criar Produtor Individual (Fornecedor Individual)

```bash
curl -X 'POST' \
  'http://localhost:8084/register' \
  -H 'Content-Type: application/json' \
  -d '{
    "tipo_usuario": "produtor",
    "subtipo_usuario": "fornecedor_individual",
    "name": "João Silva",
    "email": "joao.silva@example.com",
    "senha": "senha123",
    "cpf": "123.456.789-10"
}'
```

**Resposta esperada:**
```json
{
  "message": "Usuário produtor (fornecedor_individual) criado com sucesso",
  "user_id": 1,
  "tipo_usuario": "produtor",
  "subtipo_usuario": "fornecedor_individual",
  "email": "joao.silva@example.com",
  "name": "João Silva"
}
```

### 1.2. Criar Segundo Produtor (Grupo Formal)

```bash
curl -X 'POST' \
  'http://localhost:8084/register' \
  -H 'Content-Type: application/json' \
  -d '{
    "tipo_usuario": "produtor",
    "subtipo_usuario": "grupo_formal",
    "name": "Associação de Produtores ABC",
    "email": "assoc.abc@example.com",
    "senha": "senha123",
    "cnpj": "12.345.678/0001-99"
}'
```

**Resposta esperada:**
```json
{
  "message": "Usuário produtor (grupo_formal) criado com sucesso",
  "user_id": 2,
  ...
}
```

### 1.3. Criar Entidade Executora (Escola)

```bash
curl -X 'POST' \
  'http://localhost:8084/register' \
  -H 'Content-Type: application/json' \
  -d '{
    "tipo_usuario": "entidade_executora",
    "subtipo_usuario": "escola",
    "name": "Escola Estadual Exemplo",
    "email": "escola@example.com",
    "senha": "senha123",
    "nome_escola": "Escola Estadual ABC",
    "endereco": "Rua das Escolas, 123",
    "telefone": "(21) 3333-4444"
}'
```

**Resposta esperada:**
```json
{
  "message": "Usuário entidade_executora (escola) criado com sucesso",
  "user_id": 3,
  ...
}
```

## Passo 2: Obter Tokens de Autenticação

### 2.1. Login do Produtor 1

```bash
curl -X 'POST' \
  'http://localhost:8084/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=joao.silva@example.com&password=senha123'
```

**Resposta esperada:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "name": "João Silva",
  "email": "joao.silva@example.com"
}
```

**Guarde o token:** `TOKEN_PRODUTOR1=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### 2.2. Login da Entidade Executora

```bash
curl -X 'POST' \
  'http://localhost:8084/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=escola@example.com&password=senha123'
```

**Guarde o token:** `TOKEN_ENTIDADE=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

## Passo 3: Validar Documentos (CPF/CNPJ)

### 3.1. Validar CPF (deve retornar false - ainda não cadastrado)

```bash
curl -X 'POST' \
  'http://localhost:8084/validar-usuario' \
  -H 'Content-Type: application/json' \
  -d '{
    "documento": "999.888.777-66"
}'
```

**Resposta esperada:**
```json
{
  "ja_cadastrado": false,
  "documento": "999.888.777-66",
  "tipo": "cpf"
}
```

### 3.2. Validar CPF já cadastrado (deve retornar true)

```bash
curl -X 'POST' \
  'http://localhost:8084/validar-usuario' \
  -H 'Content-Type: application/json' \
  -d '{
    "documento": "123.456.789-10"
}'
```

**Resposta esperada:**
```json
{
  "ja_cadastrado": true,
  "documento": "123.456.789-10",
  "tipo": "cpf"
}
```

### 3.3. Validar CNPJ

```bash
curl -X 'POST' \
  'http://localhost:8084/validar-usuario' \
  -H 'Content-Type: application/json' \
  -d '{
    "documento": "12.345.678/0001-99"
}'
```

## Passo 4: Preparar Catálogo (Produtos e Unidades)

**Nota:** Se o catálogo ainda não tiver produtos e unidades cadastrados, você precisará criá-los primeiro. Vamos assumir que já existem alguns produtos e unidades no banco.

Para verificar produtos e unidades existentes, você pode consultar diretamente no banco:

```bash
docker exec rj_devs_postgres psql -U rj_devs_user -d rj_devs_auth -c "SELECT id, nome, categoria FROM catalogo_produtos LIMIT 5;"
docker exec rj_devs_postgres psql -U rj_devs_user -d rj_devs_auth -c "SELECT id, codigo, nome FROM unidades LIMIT 5;"
```

**Exemplo de produtos e unidades que podem existir:**
- Produto ID 1: Arroz (categoria: graos)
- Produto ID 2: Feijão (categoria: graos)
- Produto ID 3: Tomate (categoria: hortifruti)
- Unidade ID 1: kg (código: kg)
- Unidade ID 2: litro (código: L)

## Passo 5: Criar Demanda Relacionando Produtos e Produtores

### 5.1. Criar Demanda com Múltiplos Produtos e Produtores

```bash
curl -X 'POST' \
  'http://localhost:8084/demandas' \
  -H 'Authorization: Bearer SEU_TOKEN_ENTIDADE' \
  -H 'Content-Type: application/json' \
  -d '{
    "titulo": "Demanda de Alimentos para Merenda Escolar - Janeiro 2025",
    "descricao": "Demanda de produtos alimentícios para merenda escolar do mês de janeiro",
    "quantidade": 1500,
    "itens": [
      {
        "produto_id": 1,
        "user_id": 1,
        "unidade_id": 1,
        "quantidade": "1000.00",
        "preco_maximo": "5.50",
        "observacoes": "Arroz tipo 1, preferencialmente orgânico"
      },
      {
        "produto_id": 3,
        "user_id": 2,
        "unidade_id": 1,
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
}'
```

**Resposta esperada:**
```json
{
  "id": 1,
  "organizacao_id": null,
  "titulo": "Demanda de Alimentos para Merenda Escolar - Janeiro 2025",
  "descricao": "Demanda de produtos alimentícios...",
  "quantidade": 1500,
  "status": "draft",
  "criada_por_user_id": 3,
  "versao_atual": 1,
  "itens": [
    {
      "id": 1,
      "produto_id": 1,
      "user_id": 1,
      "user_nome": "João Silva",
      "unidade_id": 1,
      "quantidade": "1000.00",
      "preco_maximo": "5.50",
      "observacoes": "Arroz tipo 1...",
      "produto_nome": "Arroz",
      "unidade_nome": "kg"
    },
    {
      "id": 2,
      "produto_id": 3,
      "user_id": 2,
      "user_nome": "Associação de Produtores ABC",
      "unidade_id": 1,
      "quantidade": "500.00",
      "preco_maximo": "8.00",
      "observacoes": "Tomate vermelho...",
      "produto_nome": "Tomate",
      "unidade_nome": "kg"
    }
  ]
}
```

## Passo 6: Listar Demandas

### 6.1. Listar Todas as Demandas

```bash
curl -X 'GET' \
  'http://localhost:8084/demandas' \
  -H 'Authorization: Bearer SEU_TOKEN_ENTIDADE'
```

### 6.2. Filtrar por Status

```bash
curl -X 'GET' \
  'http://localhost:8084/demandas?status=draft' \
  -H 'Authorization: Bearer SEU_TOKEN_ENTIDADE'
```

## Passo 7: Obter Demanda Específica

```bash
curl -X 'GET' \
  'http://localhost:8084/demandas/1' \
  -H 'Authorization: Bearer SEU_TOKEN_ENTIDADE'
```

## Passo 8: Listar Produtores que Podem Suprir uma Demanda

```bash
curl -X 'GET' \
  'http://localhost:8084/demandas/1/produtores' \
  -H 'Authorization: Bearer SEU_TOKEN_ENTIDADE'
```

**Resposta esperada:**
```json
[
  {
    "produtor_id": 1,
    "user_id": 1,
    "nome_produtor": "João Silva",
    "email": "joao.silva@example.com",
    "tipo_produtor": "individual",
    "itens_disponiveis": [
      {
        "produto_id": 1,
        "produto_nome": "Arroz",
        "unidade_id": 1,
        "unidade_nome": "kg",
        "quantidade_disponivel": "2000.00",
        "preco_base": "5.00"
      }
    ],
    "percentual_cobertura": 50.0,
    "total_itens_demanda": 2,
    "itens_supriveis": 1
  }
]
```

## Script Completo de Teste

Aqui está um script bash completo que executa todo o fluxo:

```bash
#!/bin/bash

BASE_URL="http://localhost:8084"

echo "=== PASSO 1: Criando Usuários ==="

# Criar Produtor 1
echo "Criando Produtor 1..."
PRODUTOR1_RESPONSE=$(curl -s -X 'POST' \
  "${BASE_URL}/register" \
  -H 'Content-Type: application/json' \
  -d '{
    "tipo_usuario": "produtor",
    "subtipo_usuario": "fornecedor_individual",
    "name": "João Silva",
    "email": "joao.silva@example.com",
    "senha": "senha123",
    "cpf": "123.456.789-10"
}')
echo $PRODUTOR1_RESPONSE | jq '.'
PRODUTOR1_ID=$(echo $PRODUTOR1_RESPONSE | jq -r '.user_id')

# Criar Produtor 2
echo "Criando Produtor 2..."
PRODUTOR2_RESPONSE=$(curl -s -X 'POST' \
  "${BASE_URL}/register" \
  -H 'Content-Type: application/json' \
  -d '{
    "tipo_usuario": "produtor",
    "subtipo_usuario": "grupo_formal",
    "name": "Associação ABC",
    "email": "assoc.abc@example.com",
    "senha": "senha123",
    "cnpj": "12.345.678/0001-99"
}')
echo $PRODUTOR2_RESPONSE | jq '.'
PRODUTOR2_ID=$(echo $PRODUTOR2_RESPONSE | jq -r '.user_id')

# Criar Entidade Executora
echo "Criando Entidade Executora..."
ENTIDADE_RESPONSE=$(curl -s -X 'POST' \
  "${BASE_URL}/register" \
  -H 'Content-Type: application/json' \
  -d '{
    "tipo_usuario": "entidade_executora",
    "subtipo_usuario": "escola",
    "name": "Escola Estadual Exemplo",
    "email": "escola@example.com",
    "senha": "senha123",
    "nome_escola": "Escola Estadual ABC"
}')
echo $ENTIDADE_RESPONSE | jq '.'
ENTIDADE_ID=$(echo $ENTIDADE_RESPONSE | jq -r '.user_id')

echo ""
echo "=== PASSO 2: Obtendo Tokens ==="

# Login Entidade
echo "Fazendo login da entidade..."
TOKEN_ENTIDADE=$(curl -s -X 'POST' \
  "${BASE_URL}/token" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=escola@example.com&password=senha123' | jq -r '.access_token')
echo "Token obtido: ${TOKEN_ENTIDADE:0:20}..."

echo ""
echo "=== PASSO 3: Validando Documentos ==="

# Validar CPF não cadastrado
echo "Validando CPF não cadastrado..."
curl -s -X 'POST' \
  "${BASE_URL}/validar-usuario" \
  -H 'Content-Type: application/json' \
  -d '{"documento": "999.888.777-66"}' | jq '.'

# Validar CPF cadastrado
echo "Validando CPF cadastrado..."
curl -s -X 'POST' \
  "${BASE_URL}/validar-usuario" \
  -H 'Content-Type: application/json' \
  -d '{"documento": "123.456.789-10"}' | jq '.'

echo ""
echo "=== PASSO 4: Criando Demanda ==="

# Criar Demanda
echo "Criando demanda com múltiplos produtos e produtores..."
DEMANDA_RESPONSE=$(curl -s -X 'POST' \
  "${BASE_URL}/demandas" \
  -H "Authorization: Bearer ${TOKEN_ENTIDADE}" \
  -H 'Content-Type: application/json' \
  -d "{
    \"titulo\": \"Demanda de Alimentos - Janeiro 2025\",
    \"descricao\": \"Demanda de produtos alimentícios\",
    \"quantidade\": 1500,
    \"itens\": [
      {
        \"produto_id\": 1,
        \"user_id\": ${PRODUTOR1_ID},
        \"unidade_id\": 1,
        \"quantidade\": \"1000.00\",
        \"preco_maximo\": \"5.50\",
        \"observacoes\": \"Arroz tipo 1\"
      },
      {
        \"produto_id\": 3,
        \"user_id\": ${PRODUTOR2_ID},
        \"unidade_id\": 1,
        \"quantidade\": \"500.00\",
        \"preco_maximo\": \"8.00\",
        \"observacoes\": \"Tomate vermelho\"
      }
    ],
    \"encerra_em\": \"2025-01-15T23:59:59\"
  }")
echo $DEMANDA_RESPONSE | jq '.'
DEMANDA_ID=$(echo $DEMANDA_RESPONSE | jq -r '.id')

echo ""
echo "=== PASSO 5: Listando Demandas ==="
curl -s -X 'GET' \
  "${BASE_URL}/demandas" \
  -H "Authorization: Bearer ${TOKEN_ENTIDADE}" | jq '.'

echo ""
echo "=== PASSO 6: Obtendo Demanda Específica ==="
curl -s -X 'GET' \
  "${BASE_URL}/demandas/${DEMANDA_ID}" \
  -H "Authorization: Bearer ${TOKEN_ENTIDADE}" | jq '.'

echo ""
echo "=== PASSO 7: Listando Produtores que Podem Suprir ==="
curl -s -X 'GET' \
  "${BASE_URL}/demandas/${DEMANDA_ID}/produtores" \
  -H "Authorization: Bearer ${TOKEN_ENTIDADE}" | jq '.'

echo ""
echo "=== TESTE COMPLETO FINALIZADO ==="
```

## Validações Importantes

### ✅ Validações que Funcionam

1. **CPF/CNPJ já cadastrado**: O endpoint `/validar-usuario` retorna `true` se o documento já existe
2. **Tipo de usuário**: Ao criar demanda, valida que cada `user_id` nos itens é do tipo `'produtor'`
3. **Produtos e unidades**: Valida que produtos e unidades existem no catálogo
4. **Múltiplos relacionamentos**: Uma demanda pode ter N itens, cada um relacionando produto + produtor

### ⚠️ Pontos de Atenção

1. **Produtos e Unidades**: Certifique-se de que existem produtos e unidades no catálogo antes de criar demandas
2. **Tokens**: Use o token correto para cada operação (entidade para criar demandas, produtor para outras operações)
3. **IDs**: Os IDs retornados nas respostas podem variar, ajuste os exemplos conforme necessário

## Exemplo de Estrutura Final

Após executar o fluxo completo, você terá:

- **Demanda ID 1**:
  - Item 1: Produto 1 (Arroz) → Produtor 1 (João Silva) → Quantidade 1000
  - Item 2: Produto 3 (Tomate) → Produtor 2 (Associação ABC) → Quantidade 500

Isso demonstra que uma demanda pode relacionar múltiplos produtos com múltiplos produtores diferentes.

## Resumo Executivo

### Estrutura de Dados Criada

Após executar o fluxo completo, você terá:

1. **Usuários criados:**
   - Produtor 1 (ID: 1) - João Silva - CPF: 123.456.789-10
   - Produtor 2 (ID: 2) - Associação ABC - CNPJ: 12.345.678/0001-99
   - Entidade (ID: 3) - Escola Estadual

2. **Demanda criada (ID: 1):**
   - Item 1: Produto 1 (Arroz) → Produtor 1 (João Silva) → Quantidade: 1000 kg
   - Item 2: Produto 3 (Tomate) → Produtor 2 (Associação ABC) → Quantidade: 500 kg

### Validações Testadas

✅ **Validação de CPF/CNPJ**: Endpoint `/validar-usuario` funciona corretamente
✅ **Validação de tipo de usuário**: Valida que `user_id` nos itens é do tipo `'produtor'`
✅ **Múltiplos relacionamentos**: Uma demanda pode ter N produtos de N produtores
✅ **Estrutura de dados**: Cada item relaciona produto + produtor + quantidade

### Executar Teste Rápido

Para executar um teste rápido, use o script:

```bash
./exemplo_teste_rapido.sh
```

Ou execute o teste completo:

```bash
./teste_completo.sh
```

### Notas Importantes

1. **Catálogo**: O catálogo já foi populado com produtos e unidades básicos
2. **IDs**: Os IDs podem variar conforme dados existentes no banco
3. **Tokens**: Use tokens válidos para operações autenticadas
4. **Validações**: Todos os `user_id` nos itens devem ser do tipo `'produtor'`

