-- Script de inicialização do banco de dados
-- Este arquivo é referência da estrutura. As tabelas são criadas automaticamente
-- pelo SQLAlchemy ORM na inicialização da aplicação via db.py:create_tables()

-- Tabela de usuários (base para todas as contas)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hash_senha VARCHAR(255) NOT NULL,
    role VARCHAR(100),
    tipo_usuario VARCHAR(50) NOT NULL,
    subtipo_usuario VARCHAR(50) NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de fornecedores individuais (produtor > fornecedor_individual)
CREATE TABLE IF NOT EXISTS fornecedores_individuais (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela de grupos informais (produtor > grupo_informal)
CREATE TABLE IF NOT EXISTS grupos_informais (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    participantes JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela de grupos formais (produtor > grupo_formal)
CREATE TABLE IF NOT EXISTS grupos_formais (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    cnpj VARCHAR(18) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela de escolas (entidade_executora > escola)
CREATE TABLE IF NOT EXISTS escolas (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    nome_escola VARCHAR(255) NOT NULL,
    endereco TEXT,
    telefone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela de governos (entidade_executora > governo)
CREATE TABLE IF NOT EXISTS governos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    nome_orgao VARCHAR(255) NOT NULL,
    nivel VARCHAR(50) NOT NULL,
    endereco TEXT,
    telefone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabela de produtos (para qualquer usuário)
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

-- Tabela de documentos do usuário (para produtores)
CREATE TABLE IF NOT EXISTS documentos_usuario (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    nome_documento VARCHAR(255) NOT NULL,
    descricao TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    caminho_arquivo VARCHAR(500),
    data_envio TIMESTAMP,
    observacoes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================================
-- NOVOS MODELOS - MVP FASE 1
-- ============================================================================

-- Tabelas Base (Organizações, Catálogo, Tipos de Documento)
CREATE TABLE IF NOT EXISTS organizacoes (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    identificacao_legal VARCHAR(50),
    endereco_json JSONB,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS usuarios_governo (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    organizacao_id INTEGER NOT NULL REFERENCES organizacoes(id),
    cargo VARCHAR(255),
    permissoes_json JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS unidades (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS catalogo_produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    unidade_padrao_id INTEGER NOT NULL REFERENCES unidades(id),
    ativo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sinonimos_produtos (
    id SERIAL PRIMARY KEY,
    produto_id INTEGER NOT NULL REFERENCES catalogo_produtos(id) ON DELETE CASCADE,
    sinonimo VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS substituicoes_equivalencias (
    id SERIAL PRIMARY KEY,
    from_product_id INTEGER NOT NULL REFERENCES catalogo_produtos(id),
    to_product_id INTEGER NOT NULL REFERENCES catalogo_produtos(id),
    razao_equivalencia VARCHAR(20),
    observacoes VARCHAR(500),
    ativo BOOLEAN DEFAULT true,
    aprovado_por_user_id INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tipos_documentos (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    requerido_para_json JSONB,
    validade_dias INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS arquivos (
    id SERIAL PRIMARY KEY,
    nome_original VARCHAR(500) NOT NULL,
    caminho_storage VARCHAR(500) NOT NULL,
    mime_type VARCHAR(100),
    tamanho_bytes BIGINT,
    hash_arquivo VARCHAR(255),
    uploaded_by_user_id INTEGER REFERENCES users(id),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Perfil Produtor e Documentação
CREATE TABLE IF NOT EXISTS perfis_produtores (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    tipo_produtor VARCHAR(50) NOT NULL,
    identificacao_legal VARCHAR(50),
    rg_ie VARCHAR(50),
    endereco_json JSONB,
    capacidades_entrega_json JSONB,
    status_perfil VARCHAR(50) DEFAULT 'incomplete',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS documentos_produtor (
    id SERIAL PRIMARY KEY,
    produtor_id INTEGER NOT NULL REFERENCES perfis_produtores(id) ON DELETE CASCADE,
    tipo_documento_id INTEGER NOT NULL REFERENCES tipos_documentos(id),
    status VARCHAR(50) DEFAULT 'pending',
    reviewed_by_user_id INTEGER REFERENCES users(id),
    reviewed_at TIMESTAMP,
    rejection_reason TEXT,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS arquivos_documentos (
    id SERIAL PRIMARY KEY,
    documento_produtor_id INTEGER NOT NULL REFERENCES documentos_produtor(id) ON DELETE CASCADE,
    arquivo_id INTEGER NOT NULL REFERENCES arquivos(id),
    versao INTEGER NOT NULL,
    uploaded_by_user_id INTEGER REFERENCES users(id),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workflows_documentos (
    id SERIAL PRIMARY KEY,
    produtor_id INTEGER NOT NULL REFERENCES perfis_produtores(id) ON DELETE CASCADE,
    tipo_documento_id INTEGER NOT NULL REFERENCES tipos_documentos(id),
    status VARCHAR(50) DEFAULT 'not_started',
    etapa_atual INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS etapas_workflows (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER NOT NULL REFERENCES workflows_documentos(id) ON DELETE CASCADE,
    numero_etapa INTEGER NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    status VARCHAR(50) DEFAULT 'todo',
    arquivo_evidencia_id INTEGER REFERENCES arquivos(id),
    concluida_em TIMESTAMP
);

-- Produção e Capacidade
CREATE TABLE IF NOT EXISTS itens_producao (
    id SERIAL PRIMARY KEY,
    produtor_id INTEGER NOT NULL REFERENCES perfis_produtores(id) ON DELETE CASCADE,
    produto_id INTEGER NOT NULL REFERENCES catalogo_produtos(id),
    unidade_id INTEGER NOT NULL REFERENCES unidades(id),
    preco_base NUMERIC(10, 2),
    observacoes TEXT,
    ativo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS periodos_capacidade (
    id SERIAL PRIMARY KEY,
    item_producao_id INTEGER NOT NULL REFERENCES itens_producao(id) ON DELETE CASCADE,
    tipo_periodo VARCHAR(50) NOT NULL,
    periodo_inicio DATE NOT NULL,
    periodo_fim DATE NOT NULL,
    quantidade_capacidade NUMERIC(10, 2) NOT NULL,
    quantidade_previsao NUMERIC(10, 2),
    updated_by_user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Demandas/Editais
CREATE TABLE IF NOT EXISTS demandas (
    id SERIAL PRIMARY KEY,
    organizacao_id INTEGER NOT NULL REFERENCES organizacoes(id),
    titulo VARCHAR(500) NOT NULL,
    descricao TEXT,
    status VARCHAR(50) DEFAULT 'draft',
    publicada_em TIMESTAMP,
    encerra_em TIMESTAMP,
    local_entrega_json JSONB,
    criada_por_user_id INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS versoes_demanda (
    id SERIAL PRIMARY KEY,
    demanda_id INTEGER NOT NULL REFERENCES demandas(id) ON DELETE CASCADE,
    numero_versao INTEGER NOT NULL,
    tipo_fonte VARCHAR(50) DEFAULT 'manual',
    texto_original TEXT,
    arquivo_original_id INTEGER REFERENCES arquivos(id),
    confianca_estruturada_json JSONB,
    criada_por_user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(demanda_id, numero_versao)
);

CREATE TABLE IF NOT EXISTS itens_demanda (
    id SERIAL PRIMARY KEY,
    versao_demanda_id INTEGER NOT NULL REFERENCES versoes_demanda(id) ON DELETE CASCADE,
    produto_id INTEGER NOT NULL REFERENCES catalogo_produtos(id),
    unidade_id INTEGER NOT NULL REFERENCES unidades(id),
    quantidade NUMERIC(10, 2) NOT NULL,
    cronograma_entrega_json JSONB,
    preco_maximo NUMERIC(10, 2),
    observacoes TEXT
);

CREATE TABLE IF NOT EXISTS requisitos_demanda (
    id SERIAL PRIMARY KEY,
    versao_demanda_id INTEGER NOT NULL REFERENCES versoes_demanda(id) ON DELETE CASCADE,
    tipo_requisito VARCHAR(50) NOT NULL,
    tipo_documento_id INTEGER REFERENCES tipos_documentos(id),
    descricao TEXT NOT NULL,
    obrigatorio BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Match e Grupos
CREATE TABLE IF NOT EXISTS execucoes_match (
    id SERIAL PRIMARY KEY,
    versao_demanda_id INTEGER NOT NULL REFERENCES versoes_demanda(id),
    tipo_execucao VARCHAR(50) DEFAULT 'auto',
    status VARCHAR(50) DEFAULT 'running',
    parametros_json JSONB,
    iniciada_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finalizada_em TIMESTAMP,
    criada_por_user_id INTEGER REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS candidatos_match (
    id SERIAL PRIMARY KEY,
    execucao_match_id INTEGER NOT NULL REFERENCES execucoes_match(id) ON DELETE CASCADE,
    tipo_candidato VARCHAR(50) NOT NULL,
    score_total NUMERIC(10, 2) NOT NULL,
    explicacao_json JSONB,
    percentual_cobertura NUMERIC(5, 2),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS grupos_fornecedores (
    id SERIAL PRIMARY KEY,
    versao_demanda_id INTEGER NOT NULL REFERENCES versoes_demanda(id),
    criado_de_match_id INTEGER REFERENCES execucoes_match(id),
    status VARCHAR(50) DEFAULT 'forming',
    nome_grupo VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS membros_grupos (
    id SERIAL PRIMARY KEY,
    grupo_id INTEGER NOT NULL REFERENCES grupos_fornecedores(id) ON DELETE CASCADE,
    produtor_id INTEGER NOT NULL REFERENCES perfis_produtores(id),
    papel VARCHAR(50) DEFAULT 'member',
    ingressou_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alocacoes_grupos (
    id SERIAL PRIMARY KEY,
    grupo_id INTEGER NOT NULL REFERENCES grupos_fornecedores(id) ON DELETE CASCADE,
    item_demanda_id INTEGER NOT NULL REFERENCES itens_demanda(id),
    produtor_id INTEGER NOT NULL REFERENCES perfis_produtores(id),
    quantidade_alocada NUMERIC(10, 2) NOT NULL,
    unidade_id INTEGER NOT NULL REFERENCES unidades(id),
    preco NUMERIC(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Propostas
CREATE TABLE IF NOT EXISTS propostas (
    id SERIAL PRIMARY KEY,
    versao_demanda_id INTEGER NOT NULL REFERENCES versoes_demanda(id),
    organizacao_id INTEGER NOT NULL REFERENCES organizacoes(id),
    tipo_proposta VARCHAR(50) NOT NULL,
    produtor_id INTEGER REFERENCES perfis_produtores(id),
    grupo_id INTEGER REFERENCES grupos_fornecedores(id),
    status VARCHAR(50) DEFAULT 'draft',
    valor_total NUMERIC(12, 2),
    criada_por_user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS itens_proposta (
    id SERIAL PRIMARY KEY,
    proposta_id INTEGER NOT NULL REFERENCES propostas(id) ON DELETE CASCADE,
    item_demanda_id INTEGER NOT NULL REFERENCES itens_demanda(id),
    produto_id INTEGER NOT NULL REFERENCES catalogo_produtos(id),
    unidade_id INTEGER NOT NULL REFERENCES unidades(id),
    quantidade NUMERIC(10, 2) NOT NULL,
    preco NUMERIC(10, 2),
    substituto_de_produto_id INTEGER REFERENCES catalogo_produtos(id),
    motivo_substituicao TEXT,
    flag_aviso BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS confirmacoes_participantes (
    id SERIAL PRIMARY KEY,
    proposta_id INTEGER NOT NULL REFERENCES propostas(id) ON DELETE CASCADE,
    produtor_id INTEGER NOT NULL REFERENCES perfis_produtores(id),
    status VARCHAR(50) DEFAULT 'invited',
    motivo_recusa TEXT,
    convidado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    respondido_em TIMESTAMP,
    expira_em TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reservas_capacidade (
    id SERIAL PRIMARY KEY,
    produtor_id INTEGER NOT NULL REFERENCES perfis_produtores(id),
    proposta_id INTEGER NOT NULL REFERENCES propostas(id),
    demanda_id INTEGER NOT NULL REFERENCES demandas(id),
    periodo_inicio DATE NOT NULL,
    periodo_fim DATE NOT NULL,
    quantidades_reservadas_json JSONB,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Submissão
CREATE TABLE IF NOT EXISTS submissoes_propostas (
    id SERIAL PRIMARY KEY,
    proposta_id INTEGER NOT NULL UNIQUE REFERENCES propostas(id) ON DELETE CASCADE,
    tipo_submissao VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'not_started',
    submetida_em TIMESTAMP,
    arquivo_comprovante_id INTEGER REFERENCES arquivos(id),
    observacoes TEXT
);

CREATE TABLE IF NOT EXISTS etapas_submissao_fisica (
    id SERIAL PRIMARY KEY,
    submissao_proposta_id INTEGER NOT NULL REFERENCES submissoes_propostas(id) ON DELETE CASCADE,
    numero_etapa INTEGER NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    status VARCHAR(50) DEFAULT 'todo',
    arquivo_evidencia_id INTEGER REFERENCES arquivos(id),
    concluida_em TIMESTAMP
);

-- Decisão e Contratos
CREATE TABLE IF NOT EXISTS decisoes_propostas (
    id SERIAL PRIMARY KEY,
    proposta_id INTEGER NOT NULL REFERENCES propostas(id),
    decidida_por_user_id INTEGER NOT NULL REFERENCES users(id),
    decisao VARCHAR(50) NOT NULL,
    justificativa TEXT,
    decidida_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS modelos_contrato (
    id SERIAL PRIMARY KEY,
    organizacao_id INTEGER NOT NULL REFERENCES organizacoes(id),
    nome VARCHAR(255) NOT NULL,
    numero_versao INTEGER NOT NULL,
    arquivo_template_id INTEGER NOT NULL REFERENCES arquivos(id),
    ativo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS contratos (
    id SERIAL PRIMARY KEY,
    organizacao_id INTEGER NOT NULL REFERENCES organizacoes(id),
    demanda_id INTEGER NOT NULL REFERENCES demandas(id),
    proposta_id INTEGER NOT NULL REFERENCES propostas(id),
    modelo_id INTEGER REFERENCES modelos_contrato(id),
    status VARCHAR(50) DEFAULT 'draft',
    arquivo_contrato_id INTEGER REFERENCES arquivos(id),
    gerado_em TIMESTAMP,
    assinado_em TIMESTAMP
);

-- Auditoria e Sistema
CREATE TABLE IF NOT EXISTS eventos_auditoria (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    tipo_evento VARCHAR(100) NOT NULL,
    entidade_tipo VARCHAR(100),
    entidade_id INTEGER,
    dados_antes_json JSONB,
    dados_depois_json JSONB,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS notificacoes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tipo VARCHAR(100) NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    mensagem TEXT NOT NULL,
    link VARCHAR(500),
    lida BOOLEAN DEFAULT false,
    lida_em TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- ÍNDICES PARA PERFORMANCE
-- ============================================================================

-- Índices originais
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_tipo_usuario ON users(tipo_usuario);
CREATE INDEX IF NOT EXISTS idx_fornecedores_user_id ON fornecedores_individuais(user_id);
CREATE INDEX IF NOT EXISTS idx_grupos_informais_user_id ON grupos_informais(user_id);
CREATE INDEX IF NOT EXISTS idx_grupos_formais_user_id ON grupos_formais(user_id);
CREATE INDEX IF NOT EXISTS idx_escolas_user_id ON escolas(user_id);
CREATE INDEX IF NOT EXISTS idx_governos_user_id ON governos(user_id);
CREATE INDEX IF NOT EXISTS idx_produtos_user_id ON produtos(user_id);
CREATE INDEX IF NOT EXISTS idx_documentos_user_id ON documentos_usuario(user_id);
CREATE INDEX IF NOT EXISTS idx_documentos_status ON documentos_usuario(status);

-- Índices novos
CREATE INDEX IF NOT EXISTS idx_organizacoes_tipo ON organizacoes(tipo);
CREATE INDEX IF NOT EXISTS idx_usuarios_governo_user_id ON usuarios_governo(user_id);
CREATE INDEX IF NOT EXISTS idx_usuarios_governo_org_id ON usuarios_governo(organizacao_id);
CREATE INDEX IF NOT EXISTS idx_unidades_codigo ON unidades(codigo);
CREATE INDEX IF NOT EXISTS idx_catalogo_produtos_nome ON catalogo_produtos(nome);
CREATE INDEX IF NOT EXISTS idx_catalogo_produtos_categoria ON catalogo_produtos(categoria);
CREATE INDEX IF NOT EXISTS idx_sinonimos_produto_id ON sinonimos_produtos(produto_id);
CREATE INDEX IF NOT EXISTS idx_sinonimos_sinonimo ON sinonimos_produtos(sinonimo);
CREATE INDEX IF NOT EXISTS idx_tipos_documentos_codigo ON tipos_documentos(codigo);
CREATE INDEX IF NOT EXISTS idx_arquivos_hash ON arquivos(hash_arquivo);
CREATE INDEX IF NOT EXISTS idx_perfis_produtores_user_id ON perfis_produtores(user_id);
CREATE INDEX IF NOT EXISTS idx_perfis_produtores_status ON perfis_produtores(status_perfil);
CREATE INDEX IF NOT EXISTS idx_docs_produtor_produtor_id ON documentos_produtor(produtor_id);
CREATE INDEX IF NOT EXISTS idx_docs_produtor_tipo ON documentos_produtor(tipo_documento_id);
CREATE INDEX IF NOT EXISTS idx_docs_produtor_status ON documentos_produtor(status);
CREATE INDEX IF NOT EXISTS idx_arq_docs_documento_id ON arquivos_documentos(documento_produtor_id);
CREATE INDEX IF NOT EXISTS idx_wf_docs_produtor_id ON workflows_documentos(produtor_id);
CREATE INDEX IF NOT EXISTS idx_itens_prod_produtor_id ON itens_producao(produtor_id);
CREATE INDEX IF NOT EXISTS idx_itens_prod_produto_id ON itens_producao(produto_id);
CREATE INDEX IF NOT EXISTS idx_per_cap_item_prod_id ON periodos_capacidade(item_producao_id);
CREATE INDEX IF NOT EXISTS idx_per_cap_periodo ON periodos_capacidade(periodo_inicio, periodo_fim);
CREATE INDEX IF NOT EXISTS idx_demandas_org_id ON demandas(organizacao_id);
CREATE INDEX IF NOT EXISTS idx_demandas_status ON demandas(status);
CREATE INDEX IF NOT EXISTS idx_demandas_encerra_em ON demandas(encerra_em);
CREATE INDEX IF NOT EXISTS idx_versoes_dem_demanda_id ON versoes_demanda(demanda_id);
CREATE INDEX IF NOT EXISTS idx_itens_dem_versao_id ON itens_demanda(versao_demanda_id);
CREATE INDEX IF NOT EXISTS idx_itens_dem_produto_id ON itens_demanda(produto_id);
CREATE INDEX IF NOT EXISTS idx_req_dem_versao_id ON requisitos_demanda(versao_demanda_id);
CREATE INDEX IF NOT EXISTS idx_exec_match_versao_id ON execucoes_match(versao_demanda_id);
CREATE INDEX IF NOT EXISTS idx_exec_match_status ON execucoes_match(status);
CREATE INDEX IF NOT EXISTS idx_cand_match_exec_id ON candidatos_match(execucao_match_id);
CREATE INDEX IF NOT EXISTS idx_grupos_forn_versao_id ON grupos_fornecedores(versao_demanda_id);
CREATE INDEX IF NOT EXISTS idx_grupos_forn_status ON grupos_fornecedores(status);
CREATE INDEX IF NOT EXISTS idx_membros_grupos_grupo_id ON membros_grupos(grupo_id);
CREATE INDEX IF NOT EXISTS idx_membros_grupos_produtor_id ON membros_grupos(produtor_id);
CREATE INDEX IF NOT EXISTS idx_aloc_grupos_grupo_id ON alocacoes_grupos(grupo_id);
CREATE INDEX IF NOT EXISTS idx_aloc_grupos_item_dem_id ON alocacoes_grupos(item_demanda_id);
CREATE INDEX IF NOT EXISTS idx_propostas_versao_id ON propostas(versao_demanda_id);
CREATE INDEX IF NOT EXISTS idx_propostas_org_id ON propostas(organizacao_id);
CREATE INDEX IF NOT EXISTS idx_propostas_status ON propostas(status);
CREATE INDEX IF NOT EXISTS idx_propostas_produtor_id ON propostas(produtor_id);
CREATE INDEX IF NOT EXISTS idx_propostas_grupo_id ON propostas(grupo_id);
CREATE INDEX IF NOT EXISTS idx_itens_prop_proposta_id ON itens_proposta(proposta_id);
CREATE INDEX IF NOT EXISTS idx_itens_prop_item_dem_id ON itens_proposta(item_demanda_id);
CREATE INDEX IF NOT EXISTS idx_conf_part_proposta_id ON confirmacoes_participantes(proposta_id);
CREATE INDEX IF NOT EXISTS idx_conf_part_produtor_id ON confirmacoes_participantes(produtor_id);
CREATE INDEX IF NOT EXISTS idx_conf_part_status ON confirmacoes_participantes(status);
CREATE INDEX IF NOT EXISTS idx_res_cap_produtor_id ON reservas_capacidade(produtor_id);
CREATE INDEX IF NOT EXISTS idx_res_cap_proposta_id ON reservas_capacidade(proposta_id);
CREATE INDEX IF NOT EXISTS idx_res_cap_periodo ON reservas_capacidade(periodo_inicio, periodo_fim);
CREATE INDEX IF NOT EXISTS idx_sub_prop_proposta_id ON submissoes_propostas(proposta_id);
CREATE INDEX IF NOT EXISTS idx_sub_prop_status ON submissoes_propostas(status);
CREATE INDEX IF NOT EXISTS idx_etapas_sub_fis_sub_id ON etapas_submissao_fisica(submissao_proposta_id);
CREATE INDEX IF NOT EXISTS idx_dec_prop_proposta_id ON decisoes_propostas(proposta_id);
CREATE INDEX IF NOT EXISTS idx_dec_prop_decidida_por ON decisoes_propostas(decidida_por_user_id);
CREATE INDEX IF NOT EXISTS idx_mod_cont_org_id ON modelos_contrato(organizacao_id);
CREATE INDEX IF NOT EXISTS idx_contratos_org_id ON contratos(organizacao_id);
CREATE INDEX IF NOT EXISTS idx_contratos_demanda_id ON contratos(demanda_id);
CREATE INDEX IF NOT EXISTS idx_contratos_proposta_id ON contratos(proposta_id);
CREATE INDEX IF NOT EXISTS idx_contratos_status ON contratos(status);
CREATE INDEX IF NOT EXISTS idx_audit_user_id ON eventos_auditoria(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_tipo ON eventos_auditoria(tipo_evento);
CREATE INDEX IF NOT EXISTS idx_audit_entidade ON eventos_auditoria(entidade_tipo, entidade_id);
CREATE INDEX IF NOT EXISTS idx_audit_created_at ON eventos_auditoria(created_at);
CREATE INDEX IF NOT EXISTS idx_notif_user_id ON notificacoes(user_id);
CREATE INDEX IF NOT EXISTS idx_notif_lida ON notificacoes(lida);
CREATE INDEX IF NOT EXISTS idx_notif_created_at ON notificacoes(created_at);
