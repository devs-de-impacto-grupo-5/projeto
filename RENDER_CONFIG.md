# Configuração do Render - Guia Completo

## Informações para Preencher no Render

### 1. **Name** (Nome do Serviço)
```
rj-devs-impacto-api
```
ou
```
projeto-api
```
**Descrição:** Nome único para identificar seu serviço web no Render.

---

### 2. **Project** (Projeto - Opcional)
**Opção 1:** Deixar vazio por enquanto (pode criar depois)

**Opção 2:** Criar um novo projeto:
- Nome: `RJ Devs Impacto`
- Descrição: `Sistema de gestão de demandas e produtores`

**Recomendação:** Crie um projeto para organizar melhor os recursos (API, banco de dados, etc.)

---

### 3. **Language** (Linguagem/Runtime)
```
Docker
```
✅ **Já está correto!** Seu projeto usa Docker.

---

### 4. **Branch** (Branch do Git)
```
main
```
ou
```
master
```
**Verifique qual branch você está usando:**
```bash
git branch
```

**Recomendação:** Use `main` se for a branch principal do seu repositório.

---

### 5. **Region** (Região)
```
Virginia (US East)
```
ou escolha a região mais próxima dos seus usuários:
- **Oregon (US West)** - Para usuários na costa oeste dos EUA
- **Frankfurt (EU Central)** - Para usuários na Europa
- **Singapore (AP Southeast)** - Para usuários na Ásia

**Recomendação:** Se seus usuários são do Brasil, `Virginia (US East)` é uma boa opção.

---

### 6. **Root Directory** (Diretório Raiz - Opcional)
```
backend/auth
```
**⚠️ IMPORTANTE:** Como seu projeto é um monorepo (tem `backend/` e `frontend/`), você DEVE especificar o diretório raiz como `backend/auth` para que o Render:
- Execute comandos a partir desse diretório
- Use o Dockerfile correto
- Não tente fazer deploy do frontend junto

**Por que isso é necessário:**
- O Dockerfile está em `backend/auth/Dockerfile`
- O `main.py` está em `backend/auth/`
- O `requirements.txt` está em `backend/auth/`

---

### 7. **Dockerfile Path** (Caminho do Dockerfile)
```
backend/auth/Dockerfile
```
ou se você preencheu o **Root Directory** como `backend/auth`, então:
```
Dockerfile
```
(relativo ao Root Directory)

**Explicação:**
- Se **Root Directory** estiver vazio: use `backend/auth/Dockerfile`
- Se **Root Directory** = `backend/auth`: use apenas `Dockerfile`

---

## Resumo da Configuração Recomendada

### Opção 1: Com PostgreSQL Local (Docker Compose)

Para rodar PostgreSQL localmente junto com a aplicação:

| Campo | Valor |
|-------|-------|
| **Name** | `rj-devs-impacto-api` |
| **Project** | Criar novo projeto ou deixar vazio |
| **Language** | `Docker` ✅ |
| **Branch** | `main` (verificar no seu repositório) |
| **Region** | `Virginia (US East)` ou escolher outra |
| **Root Directory** | *(deixar vazio)* |
| **Dockerfile Path** | `Dockerfile` ⚠️ **Usa o Dockerfile da raiz** |

**Nota:** O Dockerfile na raiz instala e roda PostgreSQL localmente no mesmo container.

### Opção 2: PostgreSQL Separado (Recomendado para Produção)

| Campo | Valor |
|-------|-------|
| **Name** | `rj-devs-impacto-api` |
| **Project** | Criar novo projeto ou deixar vazio |
| **Language** | `Docker` ✅ |
| **Branch** | `main` (verificar no seu repositório) |
| **Region** | `Virginia (US East)` ou escolher outra |
| **Root Directory** | `backend/auth` ⚠️ **IMPORTANTE** |
| **Dockerfile Path** | `Dockerfile` (se Root Directory preenchido) ou `backend/auth/Dockerfile` |

---

## Variáveis de Ambiente Necessárias

Após criar o serviço, você precisará configurar as seguintes variáveis de ambiente no Render:

### Opção 1: Com PostgreSQL Local (Dockerfile da Raiz)

Se estiver usando o Dockerfile da raiz (PostgreSQL local), as variáveis são opcionais pois o script usa valores padrão:

```env
# Opcional - se não definir, usa valores padrão do Dockerfile
DATABASE_URL=postgresql://rj_devs_user:rj_devs_password@localhost:5432/rj_devs_auth
POSTGRES_USER=rj_devs_user
POSTGRES_PASSWORD=rj_devs_password
POSTGRES_DB=rj_devs_auth

# Obrigatórias
SECRET_KEY=sua-chave-secreta-super-segura-aqui-mude-em-producao
ALGORITHM=HS256
```

### Opção 2: Com PostgreSQL Separado (Recomendado para Render)

**⚠️ IMPORTANTE:** Use esta opção no Render. O Dockerfile em `backend/auth/Dockerfile` está configurado para usar um banco PostgreSQL externo.

Variáveis obrigatórias:
```env
DATABASE_URL=postgresql://usuario:senha@host:5432/nome_db
SECRET_KEY=sua-chave-secreta-super-segura-aqui-mude-em-producao
ALGORITHM=HS256
```

**Nota sobre DATABASE_URL:**
- No Render, após criar o serviço PostgreSQL, copie a **Internal Database URL** (não a External)
- A aplicação aguarda automaticamente o banco estar disponível antes de iniciar
- A variável `PORT` é definida automaticamente pelo Render - não precisa configurá-la manualmente

### Variáveis Opcionais (mas recomendadas):
```env
EMAIL_FROM=seu-email@gmail.com
EMAIL_PASSWORD=sua-senha-app-gmail
GEMINI_API_KEY=sua-chave-api-gemini
GEMINI_MODEL_NAME=gemini-pro
PDF_UPLOAD_DIR=storage/editais
```

### Como Configurar no Render:
1. Vá em **Environment** no painel do serviço
2. Adicione cada variável de ambiente
3. Para `DATABASE_URL`, você precisará criar um banco PostgreSQL no Render primeiro

---

## Banco de Dados PostgreSQL no Render

Você também precisará criar um serviço PostgreSQL no Render:

1. **Criar novo serviço** → **PostgreSQL**
2. **Nome:** `rj-devs-postgres`
3. **Plano:** Escolha conforme seu orçamento (Free tier disponível)
4. **Região:** Mesma região do serviço web (recomendado)
5. **Versão:** PostgreSQL 15 (ou a mais recente)

Após criar, copie a **Internal Database URL** e use como `DATABASE_URL` no serviço web.

---

## Comandos de Build (Opcional)

O Render detecta automaticamente o Dockerfile, mas você pode personalizar:

**Build Command:** (deixe vazio - Render usa Docker automaticamente)

**Start Command:** (deixe vazio - Render usa o CMD do Dockerfile)

---

## Troubleshooting

### Erro: "connection to server at localhost failed"
**Causa:** A variável `DATABASE_URL` não está configurada ou está apontando para `localhost`.

**Solução:**
1. Crie um serviço PostgreSQL no Render
2. Copie a **Internal Database URL** do serviço PostgreSQL
3. Configure `DATABASE_URL` no serviço web com essa URL

### Erro: "No open ports detected"
**Causa:** A aplicação não está escutando na porta correta.

**Solução:** O Dockerfile já está configurado para usar a variável `PORT` do Render. Verifique se:
- O Dockerfile em `backend/auth/Dockerfile` está sendo usado (não o da raiz)
- O script `start.sh` está presente e executável

## Checklist Final

Antes de fazer deploy, verifique:

- [ ] Dockerfile está em `backend/auth/Dockerfile` ✅
- [ ] `start.sh` está em `backend/auth/` ✅
- [ ] `requirements.txt` está em `backend/auth/`
- [ ] `main.py` está em `backend/auth/`
- [ ] Root Directory configurado como `backend/auth`
- [ ] Dockerfile Path configurado como `Dockerfile` (relativo ao Root Directory)
- [ ] **Banco PostgreSQL criado no Render primeiro**
- [ ] Variável `DATABASE_URL` configurada com a Internal Database URL do PostgreSQL
- [ ] Variáveis `SECRET_KEY` e `ALGORITHM` configuradas
- [ ] Repositório Git conectado ao Render

---

## Próximos Passos

1. Preencher os campos conforme este guia
2. Criar o serviço
3. Configurar variáveis de ambiente
4. Criar banco PostgreSQL
5. Fazer deploy
6. Testar a API em `https://seu-servico.onrender.com/docs`

