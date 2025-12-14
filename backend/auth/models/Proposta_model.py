# models/Proposta_model.py
from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Text, JSON, Numeric, Date, Boolean
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base


class Proposta(Base):
    """Proposta formal gerada a partir do match"""
    __tablename__ = "propostas"

    id = mapped_column(Integer, primary_key=True)
    versao_demanda_id = mapped_column(Integer, ForeignKey("versoes_demanda.id"), nullable=False)
    organizacao_id = mapped_column(Integer, ForeignKey("organizacoes.id"), nullable=False)
    tipo_proposta = mapped_column(String(50), nullable=False)  # single|group
    produtor_id = mapped_column(Integer, ForeignKey("perfis_produtores.id"), nullable=True)  # se single
    grupo_id = mapped_column(Integer, ForeignKey("grupos_fornecedores.id"), nullable=True)  # se group
    status = mapped_column(String(50), default='draft', nullable=False)  # draft|pending_validation|validated|submitted|received|selected|rejected|cancelled
    valor_total = mapped_column(Numeric(12, 2), nullable=True)
    criada_por_user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')
    updated_at = mapped_column(TIMESTAMP, server_default='NOW()', onupdate='NOW()')

    # Relacionamentos
    versao_demanda = relationship("VersaoDemanda", back_populates="propostas")
    organizacao = relationship("Organizacao", back_populates="propostas")
    produtor = relationship("PerfilProdutor", back_populates="propostas")
    grupo = relationship("GrupoFornecedor", back_populates="propostas")
    criada_por_user = relationship("User", backref="propostas_criadas")
    itens = relationship("ItemProposta", back_populates="proposta", cascade="all, delete-orphan")
    confirmacoes_participantes = relationship("ConfirmacaoParticipante", back_populates="proposta", cascade="all, delete-orphan")
    reservas_capacidade = relationship("ReservaCapacidade", back_populates="proposta", cascade="all, delete-orphan")
    submissao = relationship("SubmissaoProposta", back_populates="proposta", uselist=False, cascade="all, delete-orphan")
    decisoes = relationship("DecisaoProposta", back_populates="proposta")
    contratos = relationship("Contrato", back_populates="proposta")


class ItemProposta(Base):
    """Itens de uma proposta"""
    __tablename__ = "itens_proposta"

    id = mapped_column(Integer, primary_key=True)
    proposta_id = mapped_column(Integer, ForeignKey("propostas.id", ondelete="CASCADE"), nullable=False)
    item_demanda_id = mapped_column(Integer, ForeignKey("itens_demanda.id"), nullable=False)
    produto_id = mapped_column(Integer, ForeignKey("catalogo_produtos.id"), nullable=False)
    unidade_id = mapped_column(Integer, ForeignKey("unidades.id"), nullable=False)
    quantidade = mapped_column(Numeric(10, 2), nullable=False)
    preco = mapped_column(Numeric(10, 2), nullable=True)
    substituto_de_produto_id = mapped_column(Integer, ForeignKey("catalogo_produtos.id"), nullable=True)  # se for substituição
    motivo_substituicao = mapped_column(Text, nullable=True)
    flag_aviso = mapped_column(Boolean, default=False)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relacionamentos
    proposta = relationship("Proposta", back_populates="itens")
    item_demanda = relationship("ItemDemanda", back_populates="itens_proposta")
    produto = relationship("CatalogoProduto", foreign_keys=[produto_id], back_populates="itens_proposta")
    produto_substituto = relationship("CatalogoProduto", foreign_keys=[substituto_de_produto_id], back_populates="itens_proposta_substituto")
    unidade = relationship("Unidade", back_populates="itens_proposta")


class ConfirmacaoParticipante(Base):
    """Confirmação de participação de produtor em proposta"""
    __tablename__ = "confirmacoes_participantes"

    id = mapped_column(Integer, primary_key=True)
    proposta_id = mapped_column(Integer, ForeignKey("propostas.id", ondelete="CASCADE"), nullable=False)
    produtor_id = mapped_column(Integer, ForeignKey("perfis_produtores.id"), nullable=False)
    status = mapped_column(String(50), default='invited', nullable=False)  # invited|accepted|declined|expired
    motivo_recusa = mapped_column(Text, nullable=True)
    convidado_em = mapped_column(TIMESTAMP, server_default='NOW()')
    respondido_em = mapped_column(TIMESTAMP, nullable=True)
    expira_em = mapped_column(TIMESTAMP, nullable=True)

    # Relacionamentos
    proposta = relationship("Proposta", back_populates="confirmacoes_participantes")
    produtor = relationship("PerfilProdutor", back_populates="confirmacoes")


class ReservaCapacidade(Base):
    """Reserva de capacidade para evitar conflitos entre demandas"""
    __tablename__ = "reservas_capacidade"

    id = mapped_column(Integer, primary_key=True)
    produtor_id = mapped_column(Integer, ForeignKey("perfis_produtores.id"), nullable=False)
    proposta_id = mapped_column(Integer, ForeignKey("propostas.id"), nullable=False)
    demanda_id = mapped_column(Integer, ForeignKey("demandas.id"), nullable=False)
    periodo_inicio = mapped_column(Date, nullable=False)
    periodo_fim = mapped_column(Date, nullable=False)
    quantidades_reservadas_json = mapped_column(JSON, nullable=True)  # {produto_id: quantidade}
    status = mapped_column(String(50), default='active', nullable=False)  # active|released|expired
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')
    updated_at = mapped_column(TIMESTAMP, server_default='NOW()', onupdate='NOW()')

    # Relacionamentos
    produtor = relationship("PerfilProdutor", back_populates="reservas_capacidade")
    proposta = relationship("Proposta", back_populates="reservas_capacidade")
    demanda = relationship("Demanda", back_populates="reservas_capacidade")
