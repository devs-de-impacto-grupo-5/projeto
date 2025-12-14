# models/Submissao_model.py
from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Text, Date
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base


class SubmissaoProposta(Base):
    """Controle de submissão de proposta (digital ou física)"""
    __tablename__ = "submissoes_propostas"

    id = mapped_column(Integer, primary_key=True)
    proposta_id = mapped_column(Integer, ForeignKey("propostas.id", ondelete="CASCADE"), nullable=False, unique=True)
    tipo_submissao = mapped_column(String(50), nullable=False)  # digital|physical
    status = mapped_column(String(50), default='not_started', nullable=False)  # not_started|in_progress|submitted|failed|cancelled
    submetida_em = mapped_column(TIMESTAMP, nullable=True)
    arquivo_comprovante_id = mapped_column(Integer, ForeignKey("arquivos.id"), nullable=True)
    observacoes = mapped_column(Text, nullable=True)

    # Relacionamentos
    proposta = relationship("Proposta", back_populates="submissao")
    arquivo_comprovante = relationship("Arquivo", backref="submissoes_propostas")
    etapas_fisica = relationship("EtapaSubmissaoFisica", back_populates="submissao", cascade="all, delete-orphan")


class EtapaSubmissaoFisica(Base):
    """Etapas do checklist para submissão física"""
    __tablename__ = "etapas_submissao_fisica"

    id = mapped_column(Integer, primary_key=True)
    submissao_proposta_id = mapped_column(Integer, ForeignKey("submissoes_propostas.id", ondelete="CASCADE"), nullable=False)
    numero_etapa = mapped_column(Integer, nullable=False)
    titulo = mapped_column(String(255), nullable=False)
    descricao = mapped_column(Text, nullable=True)
    status = mapped_column(String(50), default='todo', nullable=False)  # todo|done|skipped
    arquivo_evidencia_id = mapped_column(Integer, ForeignKey("arquivos.id"), nullable=True)
    concluida_em = mapped_column(TIMESTAMP, nullable=True)

    # Relacionamentos
    submissao = relationship("SubmissaoProposta", back_populates="etapas_fisica")
    arquivo_evidencia = relationship("Arquivo", backref="etapas_submissao_fisica")
