# models/PerfilProdutor_model.py
from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base


class PerfilProdutor(Base):
    """Perfil estendido do produtor com dados adicionais"""
    __tablename__ = "perfis_produtores"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    tipo_produtor = mapped_column(String(50), nullable=False)  # individual|cooperative|association|company
    identificacao_legal = mapped_column(String(50), nullable=True)  # CPF/CNPJ
    rg_ie = mapped_column(String(50), nullable=True)
    endereco_json = mapped_column(JSON, nullable=True)  # {geo, cidade, uf, endereco, cep}
    capacidades_entrega_json = mapped_column(JSON, nullable=True)  # ["entrega_propria", "ponto_coleta"]
    status_perfil = mapped_column(String(50), default='incomplete', nullable=False)  # incomplete|complete|blocked
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')
    updated_at = mapped_column(TIMESTAMP, server_default='NOW()', onupdate='NOW()')

    # Relacionamentos
    user = relationship("User", backref="perfil_produtor")
    documentos_produtor = relationship("DocumentoProdutor", back_populates="produtor", cascade="all, delete-orphan")
    workflows_documentos = relationship("WorkflowDocumento", back_populates="produtor", cascade="all, delete-orphan")
    itens_producao = relationship("ItemProducao", back_populates="produtor", cascade="all, delete-orphan")
    propostas = relationship("Proposta", back_populates="produtor", cascade="all, delete-orphan")
    grupos_fornecedores_membros = relationship("MembroGrupo", back_populates="produtor", cascade="all, delete-orphan")
    confirmacoes = relationship("ConfirmacaoParticipante", back_populates="produtor", cascade="all, delete-orphan")
    reservas_capacidade = relationship("ReservaCapacidade", back_populates="produtor", cascade="all, delete-orphan")
