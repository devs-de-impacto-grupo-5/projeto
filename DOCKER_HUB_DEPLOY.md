# Deploy no Render usando Imagem Docker Hub

Este guia explica como fazer push de uma imagem Docker completa (aplicação + PostgreSQL) para o Docker Hub e usar no Render.

## 📦 Criando e Publicando a Imagem

### 1. Build da Imagem

```bash
# Na raiz do projeto
docker build -t seu-usuario/vitalis-api:latest .

# Ou com tag específica
docker build -t seu-usuario/vitalis-api:v1.0.0 .
```

### 2. Testar Localmente

```bash
# Rodar a imagem localmente para testar
docker run -p 8084:8084 \
  -e SECRET_KEY=sua-chave-secreta \
  -e POSTGRES_PASSWORD=senha123 \
  -e PORT=8084 \
  seu-usuario/vitalis-api:latest

# Testar se está funcionando
curl http://localhost:8084/docs
```

### 3. Login no Docker Hub

```bash
docker login
# Digite seu username e password do Docker Hub
```

### 4. Push para Docker Hub

```bash
# Push da imagem
docker push seu-usuario/vitalis-api:latest

# Ou com tag específica
docker push seu-usuario/vitalis-api:v1.0.0
```

## 🚀 Configuração no Render

### Opção 1: Usar Imagem do Docker Hub (Recomendado)

No Render, ao criar o serviço:

1. **Criar novo serviço** → **Web Service**
2. **Em vez de conectar Git**, escolha **"Use an existing Docker image"**
3. **Docker Image**: `seu-usuario/vitalis-api:latest`
4. **Configurar variáveis de ambiente** (veja abaixo)

### Opção 2: Build a partir do Dockerfile (Git)

Se preferir que o Render faça o build:

1. **Criar novo serviço** → **Web Service**
2. **Conectar repositório Git**
3. **Configurações:**
   - **Root Directory**: *(deixar vazio)*
   - **Dockerfile Path**: `Dockerfile`
4. **Configurar variáveis de ambiente**

## 🔑 Variáveis de Ambiente no Render

Configure estas variáveis no painel do Render:

### Obrigatórias

```env
SECRET_KEY=sua-chave-secreta-super-segura-aqui-mude-em-producao
ALGORITHM=HS256
```

### Opcionais (com valores padrão)

```env
POSTGRES_USER=rj_devs_user
POSTGRES_PASSWORD=rj_devs_password
POSTGRES_DB=rj_devs_auth
DATABASE_URL=postgresql://rj_devs_user:rj_devs_password@localhost:5432/rj_devs_auth
PORT=8084
```

### Adicionais

```env
EMAIL_FROM=seu-email@gmail.com
EMAIL_PASSWORD=sua-senha-app-gmail
GEMINI_API_KEY=sua-chave-api-gemini
GEMINI_MODEL_NAME=gemini-pro
PDF_UPLOAD_DIR=storage/editais
```

## ⚠️ Considerações Importantes

### Vantagens

✅ **Simplicidade**: Uma única imagem contém tudo  
✅ **Fácil deploy**: Basta fazer pull da imagem  
✅ **Consistência**: Mesmo ambiente em todos os lugares  
✅ **Testado**: Você testa a imagem completa antes de fazer push  

### Desvantagens

❌ **Dados não persistem**: O banco é recriado a cada restart do container  
❌ **Recursos compartilhados**: PostgreSQL e aplicação competem pelos mesmos recursos  
❌ **Não escalável**: Não pode escalar aplicação e banco separadamente  
❌ **Backup complexo**: Dados ficam dentro do container  

### Quando Usar

✅ **Desenvolvimento e testes**  
✅ **Demos e protótipos**  
✅ **Aplicações pequenas com poucos dados**  
❌ **Produção crítica** (use PostgreSQL gerenciado)  
❌ **Alta disponibilidade** (use serviços separados)  

## 🔄 Workflow Recomendado

### Para Desenvolvimento

```bash
# 1. Fazer mudanças no código
# 2. Build local
docker build -t seu-usuario/vitalis-api:dev .

# 3. Testar localmente
docker run -p 8084:8084 \
  -e SECRET_KEY=test \
  seu-usuario/vitalis-api:dev

# 4. Se tudo OK, fazer push
docker push seu-usuario/vitalis-api:dev
```

### Para Produção

```bash
# 1. Build com tag de versão
docker build -t seu-usuario/vitalis-api:v1.0.0 .

# 2. Testar
docker run -p 8084:8084 \
  -e SECRET_KEY=producao-secret \
  seu-usuario/vitalis-api:v1.0.0

# 3. Push
docker push seu-usuario/vitalis-api:v1.0.0

# 4. Atualizar no Render para usar a nova tag
```

## 📝 Script de Deploy Automatizado

Crie um script `deploy.sh`:

```bash
#!/bin/bash

# Configurações
DOCKER_USER="seu-usuario"
IMAGE_NAME="vitalis-api"
VERSION=${1:-latest}

echo "Building image..."
docker build -t ${DOCKER_USER}/${IMAGE_NAME}:${VERSION} .

echo "Testing image..."
docker run -d --name vitalis-test \
  -e SECRET_KEY=test \
  -p 8084:8084 \
  ${DOCKER_USER}/${IMAGE_NAME}:${VERSION}

sleep 5

echo "Checking if service is up..."
if curl -f http://localhost:8084/docs > /dev/null 2>&1; then
  echo "✅ Service is running!"
  docker stop vitalis-test
  docker rm vitalis-test
  
  echo "Pushing to Docker Hub..."
  docker push ${DOCKER_USER}/${IMAGE_NAME}:${VERSION}
  
  if [ "$VERSION" != "latest" ]; then
    docker tag ${DOCKER_USER}/${IMAGE_NAME}:${VERSION} ${DOCKER_USER}/${IMAGE_NAME}:latest
    docker push ${DOCKER_USER}/${IMAGE_NAME}:latest
  fi
  
  echo "✅ Deploy complete!"
else
  echo "❌ Service failed to start"
  docker logs vitalis-test
  docker stop vitalis-test
  docker rm vitalis-test
  exit 1
fi
```

Uso:
```bash
chmod +x deploy.sh
./deploy.sh v1.0.0
```

## 🔐 Segurança

### Não faça push de:

❌ Arquivos `.env` com credenciais reais  
❌ Chaves de API no código  
❌ Senhas hardcoded  

### Use variáveis de ambiente:

✅ Configure todas as credenciais via variáveis de ambiente no Render  
✅ Use secrets do Render para dados sensíveis  

## 📚 Referências

- [Docker Hub Documentation](https://docs.docker.com/docker-hub/)
- [Render Docker Images](https://render.com/docs/docker)
- [Docker Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)

