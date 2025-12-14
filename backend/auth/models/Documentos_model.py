# models/Documentos_model.py
from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Text, Enum
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base
import enum


class StatusDocumento(str, enum.Enum):
    """Status possível de um documento"""
    PENDING = "pending"  # Aguardando envio
    ENVIADO = "enviado"  # Enviado pelo usuário
    APROVADO = "aprovado"  # Aprovado pela administração
    REJEITADO = "rejeitado"  # Rejeitado - reenvio necessário


class DocumentoUsuario(Base):
    """Modelo para armazenar documentos requeridos do usuário produtor"""
    __tablename__ = "documentos_usuario"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    # Nome do documento (ex: "DAP Física", "CPF", etc)
    nome_documento = mapped_column(String(255), nullable=False)

    # Descrição/informações sobre o documento
    descricao = mapped_column(Text, nullable=True)

    # Status do documento
    status = mapped_column(
        String(50),
        default=StatusDocumento.PENDING,
        nullable=False
    )

    # URL/caminho do arquivo quando enviado
    caminho_arquivo = mapped_column(String(500), nullable=True)

    # Data de envio
    data_envio = mapped_column(TIMESTAMP, nullable=True)

    # Observações (motivo da rejeição, comentários, etc)
    observacoes = mapped_column(Text, nullable=True)

    # Timestamps
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')
    updated_at = mapped_column(TIMESTAMP, server_default='NOW()', onupdate='NOW()')

    # Relação com User
    user = relationship("User", back_populates="documentos")


# Mapeamento de documentos requeridos por subtipo de produtor
DOCUMENTOS_REQUERIDOS = {
    "fornecedor_individual": [
        {
            "nome": "CPF",
            "descricao": "Cópia do CPF"
        },
        {
            "nome": "DAP Física",
            "descricao": "Extrato da DAP Física (últimos 60 dias)"
        },
        {
            "nome": "Certidão Negativa Federal",
            "descricao": "Certidão Negativa (Trib. Federais e Dívida Ativa)"
        },
        {
            "nome": "Certidões Negativas Estadual/Municipal",
            "descricao": "Certidões Negativas do domicílio"
        },
        {
            "nome": "CNDT",
            "descricao": "Certidão Negativa de Débitos Trabalhistas (Justiça do Trabalho)"
        },
        {
            "nome": "Projeto de Venda",
            "descricao": "Projeto de venda assinado pelo agricultor"
        },
        {
            "nome": "Declaração de Produção",
            "descricao": "Declaração de produção própria"
        },
        {
            "nome": "Sanitário",
            "descricao": "Prova de requisitos higiênico-sanitários (se for o caso)"
        }
    ],
    "grupo_informal": [
        {
            "nome": "CPF (de cada participante)",
            "descricao": "Cópia do CPF de cada participante"
        },
        {
            "nome": "DAP Física (de cada participante)",
            "descricao": "Extrato da DAP Física de cada participante (últimos 60 dias)"
        },
        {
            "nome": "Certidão Negativa Federal",
            "descricao": "Certidão Negativa (Trib. Federais e Dívida Ativa)"
        },
        {
            "nome": "Certidões Negativas Estadual/Municipal",
            "descricao": "Certidões Negativas do domicílio"
        },
        {
            "nome": "CNDT",
            "descricao": "Certidão Negativa de Débitos Trabalhistas (Justiça do Trabalho)"
        },
        {
            "nome": "Projeto de Venda",
            "descricao": "Projeto de venda assinado por todos os agricultores"
        },
        {
            "nome": "Declaração de Produção",
            "descricao": "Declaração de que é produzido pelos participantes listados"
        },
        {
            "nome": "Sanitário",
            "descricao": "Prova de requisitos higiênico-sanitários (se for o caso)"
        }
    ],
    "grupo_formal": [
        {
            "nome": "CNPJ",
            "descricao": "Cópia do CNPJ"
        },
        {
            "nome": "DAP Jurídica",
            "descricao": "Extrato da DAP Jurídica (últimos 60 dias)"
        },
        {
            "nome": "Certidão Negativa Federal",
            "descricao": "Certidão Negativa (inclui Contribuições Sociais)"
        },
        {
            "nome": "Certidões Negativas Estadual/Municipal",
            "descricao": "Certidões Negativas do domicílio/sede"
        },
        {
            "nome": "CNDT",
            "descricao": "Certidão Negativa de Débitos Trabalhistas (Justiça do Trabalho)"
        },
        {
            "nome": "Certificado de Regularidade do FGTS",
            "descricao": "Certificado de Regularidade do FGTS"
        },
        {
            "nome": "Projeto de Venda",
            "descricao": "Projeto de venda assinado pelo representante legal"
        },
        {
            "nome": "Estatuto e Ata de Posse",
            "descricao": "Cópia do Estatuto e Ata de Posse da diretoria"
        },
        {
            "nome": "Declaração de Produção",
            "descricao": "Declaração de produção pelos associados"
        },
        {
            "nome": "Declaração de Controle de Limite",
            "descricao": "Declaração de controle do limite individual de venda"
        },
        {
            "nome": "Sanitário",
            "descricao": "Prova de requisitos higiênico-sanitários (se for o caso)"
        }
    ]
}

# Checklists para o Projeto de Venda por subtipo de produtor
PROJETO_VENDA_MODELOS = {
    "grupo_formal": {
        "titulo": "Modelo para Grupo Formal (Cooperativa/Associacao)",
        "secoes": [
            {
                "titulo": "Cabecalho",
                "itens": [
                    "Identificacao da proposta de atendimento ao Edital/Chamada Publica No"
                ]
            },
            {
                "titulo": "I - Identificacao dos Fornecedores (Grupo Formal)",
                "itens": [
                    "Nome do Proponente",
                    "CNPJ",
                    "Endereco",
                    "Municipio/UF",
                    "E-mail",
                    "DDD/Fone",
                    "CEP",
                    "No DAP Juridica",
                    "Banco",
                    "Agencia / Conta Corrente",
                    "No de Associados",
                    "No de Associados de acordo com a Lei no 11.326/2006",
                    "No de Associados com DAP Fisica",
                    "Nome do representante legal",
                    "CPF do representante",
                    "DDD/Fone do representante",
                    "Endereco do representante",
                    "Municipio/UF do representante"
                ]
            },
            {
                "titulo": "II - Identificacao da Entidade Executora do PNAE/FNDE/MEC",
                "itens": [
                    "Nome da Entidade",
                    "CNPJ",
                    "Municipio/UF",
                    "Endereco",
                    "DDD/Fone",
                    "Nome do representante e e-mail",
                    "CPF do representante da entidade"
                ]
            },
            {
                "titulo": "III - Relacao de Produtos",
                "itens": [
                    "Produto",
                    "Unidade",
                    "Quantidade",
                    "Preco de Aquisicao Unitario",
                    "Preco de Aquisicao Total",
                    "Cronograma de Entrega dos produtos"
                ]
            },
            {
                "titulo": "Assinaturas",
                "itens": [
                    "Local e Data",
                    "Assinatura do Representante do Grupo Formal",
                    "Fone/E-mail"
                ]
            }
        ]
    },
    "grupo_informal": {
        "titulo": "Modelo para Grupo Informal",
        "secoes": [
            {
                "titulo": "Cabecalho",
                "itens": [
                    "Identificacao da proposta de atendimento ao Edital/Chamada Publica No"
                ]
            },
            {
                "titulo": "I - Identificacao dos Fornecedores (Grupo Informal)",
                "itens": [
                    "Nome do Proponente",
                    "CPF",
                    "Endereco",
                    "Municipio/UF",
                    "CEP",
                    "E-mail (quando houver)",
                    "Fone",
                    "Organizado por Entidade Articuladora (Sim/Nao)",
                    "Nome da Entidade Articuladora (quando houver)",
                    "E-mail/Fone da entidade articuladora"
                ]
            },
            {
                "titulo": "II - Fornecedores Participantes",
                "itens": [
                    "Nome do Agricultor(a) Familiar",
                    "CPF",
                    "DAP",
                    "Banco",
                    "No Agencia",
                    "No Conta Corrente"
                ]
            },
            {
                "titulo": "III - Identificacao da Entidade Executora do PNAE/FNDE/MEC",
                "itens": [
                    "Nome da Entidade",
                    "CNPJ",
                    "Municipio",
                    "Endereco",
                    "DDD/Fone",
                    "Nome do representante e e-mail",
                    "CPF do representante"
                ]
            },
            {
                "titulo": "III - Relacao de Fornecedores e Produtos",
                "itens": [
                    "Identificacao do Agricultor(a) Familiar",
                    "Produto",
                    "Unidade",
                    "Quantidade",
                    "Preco de Aquisicao/Unidade",
                    "Valor Total"
                ]
            },
            {
                "titulo": "IV - Totalizacao por Produto",
                "itens": [
                    "Produto",
                    "Unidade",
                    "Quantidade",
                    "Preco/Unidade",
                    "Valor Total por Produto",
                    "Cronograma de Entrega dos Produtos",
                    "Total do projeto"
                ]
            },
            {
                "titulo": "Assinaturas",
                "itens": [
                    "Local e Data",
                    "Assinatura do Representante do Grupo Informal",
                    "Fone/E-mail e CPF do representante",
                    "Assinatura dos Agricultores(as) Fornecedores(as)"
                ]
            }
        ]
    },
    "fornecedor_individual": {
        "titulo": "Modelo para Fornecedor Individual",
        "secoes": [
            {
                "titulo": "Cabecalho",
                "itens": [
                    "Identificacao da proposta de atendimento ao Edital/Chamada Publica No"
                ]
            },
            {
                "titulo": "I - Identificacao do Fornecedor (Individual)",
                "itens": [
                    "Nome do Proponente",
                    "CPF",
                    "Endereco",
                    "Municipio/UF",
                    "CEP",
                    "No da DAP Fisica",
                    "DDD/Fone",
                    "E-mail (quando houver)",
                    "Banco",
                    "No da Agencia",
                    "No da Conta Corrente"
                ]
            },
            {
                "titulo": "II - Relacao dos Produtos",
                "itens": [
                    "Produto",
                    "Unidade",
                    "Quantidade",
                    "Preco de Aquisicao Unitario",
                    "Preco de Aquisicao Total",
                    "Cronograma de Entrega dos produtos"
                ]
            },
            {
                "titulo": "III - Identificacao da Entidade Executora do PNAE/FNDE/MEC",
                "itens": [
                    "Nome da entidade",
                    "CNPJ",
                    "Municipio",
                    "Endereco",
                    "Fone",
                    "Nome do Representante Legal",
                    "CPF do representante"
                ]
            },
            {
                "titulo": "Assinaturas",
                "itens": [
                    "Local e Data",
                    "Assinatura do Fornecedor Individual",
                    "CPF"
                ]
            }
        ]
    }
}
