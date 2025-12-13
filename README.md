# RJ Devs - Sistema de Autenticação e Autorização

Sistema simples de login e autorização de usuário com FastAPI, PostgreSQL e JWT.

## Estrutura do Projeto

```
projeto/
├── backend/
│   └── auth/          # API de autenticação com FastAPI
├── frontend/          # Frontend React (a ser implementado)
├── docker-compose.yml # Configuração dos serviços
├── .env               # Variáveis de ambiente (local)
└── .env.example       # Exemplo de variáveis de ambiente
```

## Tecnologias Utilizadas

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Autenticação**: JWT (JSON Web Tokens)
- **Containerização**: Docker + Docker Compose
- **ORM**: SQLAlchemy 2.0

## Como Começar

### 1. Pré-requisitos

- Docker e Docker Compose instalados

### 2. Setup Inicial

```bash
cd projeto

# Copie as variáveis de ambiente (opcional, já existe .env padrão)
cp .env.example .env
```

### 3. Iniciar os Serviços

```bash
# Inicie os serviços com Docker Compose
docker compose up -d

# Verifique se está tudo rodando
docker compose ps
```

### 4. Acessar a API

- **URL Base**: http://localhost:8084
- **Documentação Swagger**: http://localhost:8084/docs
- **Documentação ReDoc**: http://localhost:8084/redoc

## Endpoints da API

### Autenticação

#### Registrar Usuário
```bash
POST /api/auth/registrar
Content-Type: application/json

{
  "name": "João Silva",
  "email": "joao@example.com",
  "senha": "senha123",
  "role": "admin"
}
```

**Nota**: O campo `role` é opcional e aceita qualquer string. Se não for fornecido, será `null`.

#### Login
```bash
POST /api/auth/token
Content-Type: application/x-www-form-urlencoded

username=joao@example.com&password=senha123
```

Resposta:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user_id": 1,
  "role": "admin",
  "name": "João Silva",
  "email": "joao@example.com"
}
```

#### Listar Usuários
```bash
GET /api/auth/usuarios
```

#### Obter Usuário por ID
```bash
GET /api/auth/usuarios/{user_id}
```

#### Solicitar Redefinição de Senha
```bash
POST /api/auth/solicitar-redefinicao-senha
Content-Type: application/json

{
  "email": "joao@example.com"
}
```

#### Redefinir Senha
```bash
POST /api/auth/redefinir-senha
Content-Type: application/json

{
  "token": "token-de-redefinicao",
  "new_password": "nova-senha"
}
```

## Roles de Usuário

O campo `role` é completamente flexível e aceita qualquer string. Exemplos:

- `admin` - Administrador
- `user` - Usuário comum
- `moderator` - Moderador
- Qualquer outra string que faça sentido para sua aplicação
- `null` - Se não fornecer um role

Use a função `require_role("seu_role")` para proteger endpoints específicos.

## Variáveis de Ambiente

Edite o arquivo `.env` na raiz do projeto para configurar:

```env
# Database
POSTGRES_USER=rj_devs_user
POSTGRES_PASSWORD=rj_devs_password
POSTGRES_DB=rj_devs_auth

# JWT
SECRET_KEY=sua-chave-secreta-super-segura
ALGORITHM=HS256

# Email (para reset de senha)
EMAIL_FROM=seu-email@gmail.com
EMAIL_PASSWORD=sua-senha-app
```

## Comandos Úteis

```bash
# Ver logs
docker compose logs -f auth

# Ver logs do PostgreSQL
docker compose logs -f postgres

# Parar os serviços
docker compose down

# Parar e remover volumes
docker compose down -v

# Reconstruir as imagens
docker compose build --no-cache

# Executar testes (dentro do container)
docker compose exec auth pytest
```

## Desenvolvimento

### Estrutura do Backend

```
backend/auth/
├── main.py                # Aplicação principal FastAPI
├── config.py              # Configurações
├── requirements.txt       # Dependências Python
├── models/                # Modelos SQLAlchemy
│   └── User_model.py
├── schemas/               # Schemas Pydantic
│   ├── User_schema.py
│   └── Password_schema.py
├── routers/               # Rotas da API
│   └── Login_routers.py
├── security/              # Funções de segurança
│   └── security.py
├── db/                    # Configuração do banco de dados
│   ├── base.py
│   └── db.py
└── tests/                 # Testes
```

### Hot Reload

O Docker Compose está configurado com volume mount e `--reload` para desenvolvimento:

```bash
# Altere arquivos e eles serão automaticamente recarregados
# A API estará sempre sincronizada com suas mudanças
```

## Autenticação com JWT

A API usa Bearer tokens (JWT) para autenticação. Para acessar endpoints protegidos:

```bash
GET /api/auth/usuarios
Authorization: Bearer <seu-token-aqui>
```

## Proteção de Rotas com Roles

Para proteger um endpoint com um role específico:

```python
from fastapi import Depends
from security.security import require_role

@router.get("/admin-only")
async def admin_only(current_user: User = Depends(require_role("admin"))):
    return {"message": f"Bem-vindo {current_user.name}"}
```

Para verificar múltiplos roles:

```python
from security.security import require_any_role

@router.get("/staff-area")
async def staff_area(current_user: User = Depends(require_any_role(["admin", "moderator"]))):
    return {"message": "Acesso permitido"}
```
