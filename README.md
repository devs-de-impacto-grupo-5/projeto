# Vitalis - Sistema de Gestão de Demandas e Produtores

<div align="center">
  <img src="imgs/logo-vitalis.png" alt="Logo Vitalis" width="300"/>
  
  ![Vitalis](imgs/vitalis.gif)
</div>

**Vitalis** é um sistema completo para conectar entidades executoras (escolas, governos) com produtores rurais, facilitando a gestão de demandas de alimentos e produtos agrícolas.

## 🌐 Aplicação Deployada

A aplicação está disponível em produção nos seguintes links:

- **API Base**: [https://rj-devs-impacto-api.onrender.com](https://rj-devs-impacto-api.onrender.com)
- **Documentação Swagger**: [https://rj-devs-impacto-api.onrender.com/docs](https://rj-devs-impacto-api.onrender.com/docs)
- **Frontend**: [https://seu-frontend.onrender.com](https://seu-frontend.onrender.com) *(se aplicável)*

## 📋 Problema

O sistema foi desenvolvido para resolver a complexidade na gestão de demandas públicas de alimentos e produtos agrícolas, onde:

- **Entidades Executoras** (escolas, governos) precisam criar e gerenciar demandas de produtos
- **Produtores** (individuais, grupos informais e formais) precisam se cadastrar e oferecer seus produtos
- É necessário relacionar **múltiplos produtos** de **múltiplos produtores** na mesma demanda
- O sistema deve validar documentos (CPF/CNPJ) para evitar duplicatas
- É preciso um motor de matching inteligente para conectar demandas com produtores capazes de suprí-las

## 🎯 Solução Técnica

### Arquitetura

Sistema desenvolvido com **FastAPI** e **PostgreSQL**, seguindo arquitetura RESTful com separação clara de responsabilidades:

- **Backend API**: FastAPI com SQLAlchemy ORM
- **Banco de Dados**: PostgreSQL com relacionamentos complexos
- **Autenticação**: JWT (JSON Web Tokens)
- **Containerização**: Docker + Docker Compose
- **IA**: Integração com Google Gemini para processamento de editais

### Principais Funcionalidades

1. **Gestão de Usuários**
   - Cadastro de produtores (individual, grupo informal, grupo formal)
   - Cadastro de entidades executoras (escola, governo)
   - Validação de CPF/CNPJ para evitar duplicatas
   - Autenticação JWT

2. **Gestão de Demandas**
   - Criação de demandas relacionando múltiplos produtos e produtores
   - Versionamento de demandas para rastreamento de mudanças
   - Status de demanda (draft, published, closed, etc.)
   - Localização de entrega

3. **Catálogo de Produtos**
   - Catálogo centralizado de produtos
   - Unidades de medida padronizadas
   - Gestão de produção dos produtores

4. **Motor de Matching**
   - Algoritmo inteligente para conectar demandas com produtores
   - Scoring baseado em múltiplos critérios
   - Identificação de produtores capazes de suprir demandas

5. **Gestão de Propostas e Contratos**
   - Sistema de propostas dos produtores
   - Gestão de contratos
   - Confirmação de participantes

## 🛠️ Tecnologias Utilizadas

- **Backend**: FastAPI, Python 3.11
- **Banco de Dados**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Autenticação**: JWT (python-jose)
- **IA**: Google Generative AI (Gemini)
- **Containerização**: Docker, Docker Compose
- **Validação**: Pydantic
- **Testes**: Pytest, Pytest-BDD

## 🚀 Como Começar (Desenvolvimento Local)

### Pré-requisitos

- Docker e Docker Compose instalados
- Git

### Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd projeto

# Inicie os serviços
docker compose up -d

# Verifique se está tudo rodando
docker compose ps
```

### Acessar a API Local

- **URL Base**: http://localhost:8084
- **Documentação Swagger**: http://localhost:8084/docs
- **Documentação ReDoc**: http://localhost:8084/redoc

## 📁 Estrutura do Projeto

```
projeto/
├── backend/
│   └── auth/              # API FastAPI
│       ├── main.py        # Aplicação principal
│       ├── models/        # Modelos SQLAlchemy
│       ├── schemas/       # Schemas Pydantic
│       ├── routers/       # Rotas da API
│       ├── services/      # Serviços (match, IA)
│       ├── db/            # Configuração do banco
│       └── tests/         # Testes
├── frontend/              # Frontend React
├── docker-compose.yml     # Configuração dos serviços
└── README.md
```

## 🔑 Variáveis de Ambiente

Configure as variáveis de ambiente no arquivo `.env`:

```env
# Database
POSTGRES_USER=rj_devs_user
POSTGRES_PASSWORD=rj_devs_password
POSTGRES_DB=rj_devs_auth

# JWT
SECRET_KEY=sua-chave-secreta-super-segura
ALGORITHM=HS256

# Email (opcional)
EMAIL_FROM=seu-email@gmail.com
EMAIL_PASSWORD=sua-senha-app

# Google Gemini AI (opcional)
GEMINI_API_KEY=sua-chave-api
GEMINI_MODEL_NAME=gemini-pro
```

## 📚 Principais Endpoints

### Autenticação
- `POST /register` - Registrar usuário
- `POST /token` - Login e obter token JWT
- `POST /validar-usuario` - Validar CPF/CNPJ

### Demandas
- `POST /demandas` - Criar demanda
- `GET /demandas` - Listar demandas
- `GET /demandas/{id}` - Obter demanda específica
- `GET /demandas/{id}/produtores` - Listar produtores que podem suprir

### Produtos
- `GET /produtos` - Listar produtos
- `POST /produtos` - Criar produto
- `PUT /produtos/{id}` - Atualizar produto

### Produtores
- `GET /produtores` - Listar produtores
- `GET /produtores/{id}` - Obter perfil do produtor

## 🧪 Testes

```bash
# Executar testes
docker compose exec auth pytest

# Executar testes com coverage
docker compose exec auth pytest --cov
```

## 📝 Comandos Úteis

```bash
# Ver logs
docker compose logs -f auth

# Parar serviços
docker compose down

# Reconstruir imagens
docker compose build --no-cache

# Acessar banco de dados
docker compose exec postgres psql -U rj_devs_user -d rj_devs_auth
```

## 👥 Equipe de Desenvolvimento

| Nome | LinkedIn |
|------|----------|
| Maurício Azevedo Neto | [LinkedIn](https://www.linkedin.com/in/mauricio-azevedo-neto/) |
| Paula Piva | [LinkedIn](https://www.linkedin.com/in/paulapiva03/) |
| Gabriel Pelinsari | [LinkedIn](https://www.linkedin.com/in/gabriel-pelinsari/) |
| Matheus Santos | [LinkedIn](https://www.linkedin.com/in/omatheusrsantos/) |

## 📄 Licença

Este projeto foi desenvolvido para o Devs Impacto.

## 🤝 Contribuindo

Este é um projeto interno. Para contribuições, entre em contato com a equipe de desenvolvimento.

---

**Vitalis** - Desenvolvido com ❤️ pela equipe Vitalis