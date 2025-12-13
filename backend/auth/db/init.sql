
-- Script de inicialização do banco de dados
-- Este arquivo será executado automaticamente quando o PostgreSQL inicia

-- Criar tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    role VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar tabela de fornecedores individuais
CREATE TABLE IF NOT EXISTS fornecedores_individuais (
    id SERIAL PRIMARY KEY,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Criar tabela de grupos informais
CREATE TABLE IF NOT EXISTS grupos_informais (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    cpfs JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Criar tabela de grupos formais
CREATE TABLE IF NOT EXISTS grupos_formais (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    cnpj VARCHAR(18) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Criar tabela de produtos
CREATE TABLE IF NOT EXISTS produtos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    categoria VARCHAR(100) NOT NULL,
    quantidade INTEGER NOT NULL,
    preco FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Criar índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_fornecedores_user_id ON fornecedores_individuais(user_id);
CREATE INDEX IF NOT EXISTS idx_grupos_informais_user_id ON grupos_informais(user_id);
CREATE INDEX IF NOT EXISTS idx_grupos_formais_user_id ON grupos_formais(user_id);
CREATE INDEX IF NOT EXISTS idx_produtos_user_id ON produtos(user_id);
