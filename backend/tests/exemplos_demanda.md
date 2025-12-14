                                                                                                                                                                                            # Exemplos de Uso - API de Demandas

## Visão Geral

A API de Demandas permite cadastrar demandas relacionando usuários (organizações) e produtos. Uma demanda pode ser suprida com **N produtos de N produtores**.

## Endpoints Disponíveis

### 1. Criar Demanda
**POST** `/demandas`

Cria uma nova demanda com seus itens (produtos necessários).

**Autenticação:** Requer token JWT

**Exemplo de requisição:**
```bash
curl -X 'POST' \
  'http://localhost:8084/demandas' \
  -H 'Authorization: Bearer SEU_TOKEN_JWT' \
  -H 'Content-Type: application/json' \
  -d '{
    "organizacao_id": 1,
    "titulo": "Demanda de Alimentos para Merenda Escolar - Janeiro 2025",
    "descricao": "Demanda de produtos alimentícios para merenda escolar do mês de janeiro",
    "itens": [
      {
        "produto_id": 1,
        "unidade_id": 1,
        "quantidade": "1000.00",
        "preco_maximo": "5.50",
        "observacoes": "Arroz tipo 1, preferencialmente orgânico"
      },
      {
        "produto_id": 2,
        "unidade_id": 2,
        "quantidade": "500.00",
        "preco_maximo": "8.00",
        "observacoes": "Feijão preto"
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

**Resposta:**
```json
{
  "id": 1,
  "organizacao_id": 1,
  "titulo": "Demanda de Alimentos para Merenda Escolar - Janeiro 2025",
  "descricao": "Demanda de produtos alimentícios...",
  "status": "draft",
  "publicada_em": null,
  "encerra_em": "2025-01-15T23:59:59",
  "local_entrega_json": {...},
  "criada_por_user_id": 1,
  "created_at": "2025-01-01T10:00:00",
  "updated_at": "2025-01-01T10:00:00",
  "versao_atual": 1,
  "itens": [
    {
      "id": 1,
      "produto_id": 1,
      "unidade_id": 1,
      "quantidade": "1000.00",
      "preco_maximo": "5.50",
      "observacoes": "Arroz tipo 1...",
      "produto_nome": "Arroz",
      "unidade_nome": "kg"
    },
    ...
  ]
}
```

### 2. Listar Demandas
**GET** `/demandas`

Lista todas as demandas, com filtros opcionais.

**Query Parameters:**
- `organizacao_id` (opcional): Filtrar por organização
- `status` (opcional): Filtrar por status (draft, published, etc)

**Exemplo:**
```bash
curl -X 'GET' \
  'http://localhost:8084/demandas?organizacao_id=1&status=draft' \
  -H 'Authorization: Bearer SEU_TOKEN_JWT'
```

### 3. Obter Demanda Específica
**GET** `/demandas/{demanda_id}`

Obtém os detalhes completos de uma demanda, incluindo todos os itens.

**Exemplo:**
```bash
curl -X 'GET' \
  'http://localhost:8084/demandas/1' \
  -H 'Authorization: Bearer SEU_TOKEN_JWT'
```

### 4. Listar Produtores que Podem Suprir uma Demanda
**GET** `/demandas/{demanda_id}/produtores`

Lista todos os produtores que podem suprir (total ou parcialmente) uma demanda.

**Retorna:**
- Lista de produtores
- Para cada produtor:
  - Quais produtos ele pode fornecer
  - Quantidade disponível
  - Preço base (se informado)
  - Capacidade por período
  - Percentual de cobertura da demanda

**Exemplo:**
```bash
curl -X 'GET' \
  'http://localhost:8084/demandas/1/produtores' \
  -H 'Authorization: Bearer SEU_TOKEN_JWT'
```

**Resposta:**
```json
[
  {
    "produtor_id": 1,
    "user_id": 5,
    "nome_produtor": "João Silva",
    "email": "joao@example.com",
    "tipo_produtor": "individual",
    "itens_disponiveis": [
      {
        "produto_id": 1,
        "produto_nome": "Arroz",
        "unidade_id": 1,
        "unidade_nome": "kg",
        "quantidade_disponivel": "2000.00",
        "preco_base": "5.00",
        "capacidade_periodo": {
          "tipo_periodo": "month",
          "periodo_inicio": "2025-01-01",
          "periodo_fim": "2025-01-31",
          "quantidade_capacidade": 2000.00
        }
      },
      {
        "produto_id": 2,
        "produto_nome": "Feijão",
        "unidade_id": 2,
        "unidade_nome": "kg",
        "quantidade_disponivel": "800.00",
        "preco_base": "7.50"
      }
    ],
    "percentual_cobertura": 100.0,
    "total_itens_demanda": 2,
    "itens_supriveis": 2
  },
  {
    "produtor_id": 2,
    "user_id": 6,
    "nome_produtor": "Maria Santos",
    "email": "maria@example.com",
    "tipo_produtor": "cooperative",
    "itens_disponiveis": [
      {
        "produto_id": 1,
        "produto_nome": "Arroz",
        "unidade_id": 1,
        "unidade_nome": "kg",
        "quantidade_disponivel": "500.00",
        "preco_base": "5.20"
      }
    ],
    "percentual_cobertura": 50.0,
    "total_itens_demanda": 2,
    "itens_supriveis": 1
  }
]
```

## Fluxo de Uso

1. **Organização cria uma demanda** com múltiplos produtos
2. **Sistema identifica produtores** que podem suprir a demanda (endpoint `/demandas/{id}/produtores`)
3. **Múltiplos produtores podem suprir** diferentes produtos da mesma demanda
4. **Sistema calcula percentual de cobertura** para cada produtor
5. **Organização pode escolher** quais produtores usar para cada produto

## Relacionamentos

- **1 Demanda** → **N Itens** (produtos necessários)
- **1 Item** → **1 Produto** (do catálogo)
- **1 Produto** → **N Produtores** (que podem fornecer)
- **1 Demanda** → **N Produtores** (que podem suprir parcial ou totalmente)

## Observações

- Uma demanda pode ser suprida por múltiplos produtores, cada um fornecendo diferentes produtos
- O sistema calcula automaticamente quais produtores podem suprir quais itens
- Produtores são ordenados por percentual de cobertura (maior primeiro)
- A capacidade de produção por período é considerada quando disponível

