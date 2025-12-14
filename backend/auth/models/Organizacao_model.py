# models/Organizacao_model.py
from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base


class Organizacao(Base):
    """Organização (município, escola, secretaria, etc)"""
    __tablename__ = "organizacoes"

    id = mapped_column(Integer, primary_key=True)
    tipo = mapped_column(String(50), nullable=False)  # municipality|school|secretariat|other
    nome = mapped_column(String(255), nullable=False)
    identificacao_legal = mapped_column(String(50), nullable=True)  # CNPJ/INEP/outro
    endereco_json = mapped_column(JSON, nullable=True)  # {cidade, uf, endereco, cep}
    status = mapped_column(String(50), default='active', nullable=False)  # active|inactive
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')
    updated_at = mapped_column(TIMESTAMP, server_default='NOW()', onupdate='NOW()')

    # Relacionamentos
    usuarios_governo = relationship("UsuarioGoverno", back_populates="organizacao", cascade="all, delete-orphan")
    demandas = relationship("Demanda", back_populates="organizacao", cascade="all, delete-orphan")
    propostas = relationship("Proposta", back_populates="organizacao", cascade="all, delete-orphan")
    contratos = relationship("Contrato", back_populates="organizacao", cascade="all, delete-orphan")
    modelos_contrato = relationship("ModeloContrato", back_populates="organizacao", cascade="all, delete-orphan")


class UsuarioGoverno(Base):
    """Usuário do governo ligado a uma organização"""
    __tablename__ = "usuarios_governo"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    organizacao_id = mapped_column(Integer, ForeignKey("organizacoes.id"), nullable=False)
    cargo = mapped_column(String(255), nullable=True)
    permissoes_json = mapped_column(JSON, nullable=True)  # permissões finas (opcional)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')
    updated_at = mapped_column(TIMESTAMP, server_default='NOW()', onupdate='NOW()')

    # Relacionamentos
    user = relationship("User", backref="usuario_governo")
    organizacao = relationship("Organizacao", back_populates="usuarios_governo")
