-- Script para popular o catálogo com produtos e unidades básicos
-- Execute este script se o catálogo estiver vazio

-- Inserir unidades básicas
INSERT INTO unidades (codigo, nome, tipo) VALUES
    ('kg', 'Quilograma', 'mass'),
    ('g', 'Grama', 'mass'),
    ('L', 'Litro', 'volume'),
    ('ml', 'Mililitro', 'volume'),
    ('un', 'Unidade', 'count'),
    ('cx', 'Caixa', 'count')
ON CONFLICT (codigo) DO NOTHING;

-- Inserir produtos básicos no catálogo
-- Nota: Ajuste os IDs das unidades conforme o que foi inserido acima
INSERT INTO catalogo_produtos (nome, categoria, unidade_padrao_id, ativo) VALUES
    ('Arroz', 'graos', (SELECT id FROM unidades WHERE codigo = 'kg'), true),
    ('Feijão', 'graos', (SELECT id FROM unidades WHERE codigo = 'kg'), true),
    ('Tomate', 'hortifruti', (SELECT id FROM unidades WHERE codigo = 'kg'), true),
    ('Cebola', 'hortifruti', (SELECT id FROM unidades WHERE codigo = 'kg'), true),
    ('Batata', 'hortifruti', (SELECT id FROM unidades WHERE codigo = 'kg'), true),
    ('Leite', 'laticinios', (SELECT id FROM unidades WHERE codigo = 'L'), true),
    ('Açúcar', 'processados', (SELECT id FROM unidades WHERE codigo = 'kg'), true),
    ('Óleo', 'processados', (SELECT id FROM unidades WHERE codigo = 'L'), true),
    ('Farinha de Trigo', 'processados', (SELECT id FROM unidades WHERE codigo = 'kg'), true),
    ('Macarrão', 'processados', (SELECT id FROM unidades WHERE codigo = 'kg'), true)
ON CONFLICT DO NOTHING;

-- Verificar o que foi inserido
SELECT 'Unidades criadas:' as info;
SELECT id, codigo, nome FROM unidades ORDER BY id;

SELECT 'Produtos criados:' as info;
SELECT cp.id, cp.nome, cp.categoria, u.codigo as unidade 
FROM catalogo_produtos cp 
JOIN unidades u ON cp.unidade_padrao_id = u.id 
ORDER BY cp.id;

