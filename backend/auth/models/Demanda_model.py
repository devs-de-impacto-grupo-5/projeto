# models/Demanda_model.py
from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Text, JSON, Numeric, Boolean, Date
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base


class Demanda(Base):
    """Demanda/Edital principal"""
    __tablename__ = "demandas"

    id = mapped_column(Integer, primary_key=True)
    organizacao_id = mapped_column(Integer, ForeignKey("organizacoes.id"), nullable=True)  # Opcional, pode ser None
    titulo = mapped_column(String(500), nullable=False)
    descricao = mapped_column(Text, nullable=True)
    quantidade = mapped_column(Integer, nullable=True)  # Quantidade total da demanda
    status = mapped_column(String(50), default='draft', nullable=False)  # draft|published|receiving_proposals|closed|cancelled|contracted
    publicada_em = mapped_column(TIMESTAMP, nullable=True)
    encerra_em = mapped_column(TIMESTAMP, nullable=True)
    local_entrega_json = mapped_column(JSON, nullable=True)  # {endereco, cidade, uf, coords}
    criada_por_user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')
    updated_at = mapped_column(TIMESTAMP, server_default='NOW()', onupdate='NOW()')

    # Relacionamentos
    organizacao = relationship("Organizacao", back_populates="demandas")
    criada_por_user = relationship("User", back_populates="demandas_criadas")
    versoes = relationship("VersaoDemanda", back_populates="demanda", cascade="all, delete-orphan")
    reservas_capacidade = relationship("ReservaCapacidade", back_populates="demanda", cascade="all, delete-orphan")
    contratos = relationship("Contrato", back_populates="demanda")


class VersaoDemanda(Base):
    """Versionamento de demandas (para rastrear mudanças)"""
    __tablename__ = "versoes_demanda"

    id = mapped_column(Integer, primary_key=True)
    demanda_id = mapped_column(Integer, ForeignKey("demandas.id", ondelete="CASCADE"), nullable=False)
    numero_versao = mapped_column(Integer, nullable=False)
    tipo_fonte = mapped_column(String(50), default='manual', nullable=False)  # manual|uploaded_document|imported
    texto_original = mapped_column(Text, nullable=True)
    arquivo_original_id = mapped_column(Integer, ForeignKey("arquivos.id"), nullable=True)
    confianca_estruturada_json = mapped_column(JSON, nullable=True)  # se vier de IA (Fase 2)
    criada_por_user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relacionamentos
    demanda = relationship("Demanda", back_populates="versoes")
    arquivo_original = relationship("Arquivo", back_populates="versoes_demanda")
    criada_por_user = relationship("User", back_populates="versoes_demanda_criadas")
    itens = relationship("ItemDemanda", back_populates="versao_demanda", cascade="all, delete-orphan")
    requisitos = relationship("RequisitoDemanda", back_populates="versao_demanda", cascade="all, delete-orphan")
    execucoes_match = relationship("ExecucaoMatch", back_populates="versao_demanda")
    propostas = relationship("Proposta", back_populates="versao_demanda")
    grupos_fornecedores = relationship("GrupoFornecedor", back_populates="versao_demanda")


class ItemDemanda(Base):
    """Itens solicitados em uma demanda"""
    __tablename__ = "itens_demanda"

    id = mapped_column(Integer, primary_key=True)
    versao_demanda_id = mapped_column(Integer, ForeignKey("versoes_demanda.id", ondelete="CASCADE"), nullable=False)
    produto_id = mapped_column(Integer, ForeignKey("catalogo_produtos.id"), nullable=False)
    unidade_id = mapped_column(Integer, ForeignKey("unidades.id"), nullable=False)
    quantidade = mapped_column(Numeric(10, 2), nullable=False)
    cronograma_entrega_json = mapped_column(JSON, nullable=True)  # parcelas/datas
    preco_maximo = mapped_column(Numeric(10, 2), nullable=True)
    observacoes = mapped_column(Text, nullable=True)

    # Relacionamentos
    versao_demanda = relationship("VersaoDemanda", back_populates="itens")
    produto = relationship("CatalogoProduto", back_populates="itens_demanda")
    unidade = relationship("Unidade", back_populates="itens_demanda")
    itens_proposta = relationship("ItemProposta", back_populates="item_demanda")
    alocacoes_grupos = relationship("AlocacaoGrupo", back_populates="item_demanda")


class RequisitoDemanda(Base):
    """Requisitos específicos de uma demanda (docs, logística, qualidade, etc)"""
    __tablename__ = "requisitos_demanda"

    id = mapped_column(Integer, primary_key=True)
    versao_demanda_id = mapped_column(Integer, ForeignKey("versoes_demanda.id", ondelete="CASCADE"), nullable=False)
    tipo_requisito = mapped_column(String(50), nullable=False)  # document|logistic|quality|other
    tipo_documento_id = mapped_column(Integer, ForeignKey("tipos_documentos.id"), nullable=True)
    descricao = mapped_column(Text, nullable=False)
    obrigatorio = mapped_column(Boolean, default=True)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relacionamentos
    versao_demanda = relationship("VersaoDemanda", back_populates="requisitos")
    tipo_documento = relationship("TipoDocumento", back_populates="requisitos_demanda")
