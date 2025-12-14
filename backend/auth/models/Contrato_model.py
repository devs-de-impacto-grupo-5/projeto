# models/Contrato_model.py
from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Text, Numeric, Boolean
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base


class DecisaoProposta(Base):
    """Decisão do governo sobre uma proposta"""
    __tablename__ = "decisoes_propostas"

    id = mapped_column(Integer, primary_key=True)
    proposta_id = mapped_column(Integer, ForeignKey("propostas.id"), nullable=False)
    decidida_por_user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    decisao = mapped_column(String(50), nullable=False)  # selected|rejected
    justificativa = mapped_column(Text, nullable=True)
    decidida_em = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relacionamentos
    proposta = relationship("Proposta", back_populates="decisoes")
    decidida_por_user = relationship("User", back_populates="decisoes_propostas")


class ModeloContrato(Base):
    """Template de contrato por organização"""
    __tablename__ = "modelos_contrato"

    id = mapped_column(Integer, primary_key=True)
    organizacao_id = mapped_column(Integer, ForeignKey("organizacoes.id"), nullable=False)
    nome = mapped_column(String(255), nullable=False)
    numero_versao = mapped_column(Integer, nullable=False)
    arquivo_template_id = mapped_column(Integer, ForeignKey("arquivos.id"), nullable=False)
    ativo = mapped_column(Boolean, default=True)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relacionamentos
    organizacao = relationship("Organizacao", back_populates="modelos_contrato")
    arquivo_template = relationship("Arquivo", back_populates="modelos_contrato")
    contratos = relationship("Contrato", back_populates="modelo")


class Contrato(Base):
    """Contrato gerado a partir de proposta vencedora"""
    __tablename__ = "contratos"

    id = mapped_column(Integer, primary_key=True)
    organizacao_id = mapped_column(Integer, ForeignKey("organizacoes.id"), nullable=False)
    demanda_id = mapped_column(Integer, ForeignKey("demandas.id"), nullable=False)
    proposta_id = mapped_column(Integer, ForeignKey("propostas.id"), nullable=False)
    modelo_id = mapped_column(Integer, ForeignKey("modelos_contrato.id"), nullable=True)
    status = mapped_column(String(50), default='draft', nullable=False)  # draft|generated|signed|cancelled
    arquivo_contrato_id = mapped_column(Integer, ForeignKey("arquivos.id"), nullable=True)
    gerado_em = mapped_column(TIMESTAMP, nullable=True)
    assinado_em = mapped_column(TIMESTAMP, nullable=True)

    # Relacionamentos
    organizacao = relationship("Organizacao", back_populates="contratos")
    demanda = relationship("Demanda", back_populates="contratos")
    proposta = relationship("Proposta", back_populates="contratos")
    modelo = relationship("ModeloContrato", back_populates="contratos")
    arquivo_contrato = relationship("Arquivo", back_populates="contratos")
    registro_blockchain = relationship("RegistroBlockchain", back_populates="contrato", uselist=False)

