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
    user = relationship("User", backref="documentos")


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
            "nome": "Requisitos Higiênico-Sanitários",
            "descricao": "Prova de requisitos higiênico-sanitários (se for o caso)"
        }
    ],
    "grupo_informal": [
        {
            "nome": "CPF dos Participantes",
            "descricao": "Cópia do CPF de cada participante"
        },
        {
            "nome": "DAP Física",
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
            "nome": "Requisitos Higiênico-Sanitários",
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
            "descricao": "Certidões Negativas da sede"
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
            "nome": "Requisitos Higiênico-Sanitários",
            "descricao": "Prova de requisitos higiênico-sanitários (se for o caso)"
        }
    ]
}
