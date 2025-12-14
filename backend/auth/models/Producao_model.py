# models/Producao_model.py
from sqlalchemy import Integer, String, ForeignKey, TIMESTAMP, Numeric, Text, Boolean, Date
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base


class ItemProducao(Base):
    """Itens que um produtor pode fornecer (usa catálogo padronizado)"""
    __tablename__ = "itens_producao"

    id = mapped_column(Integer, primary_key=True)
    produtor_id = mapped_column(Integer, ForeignKey("perfis_produtores.id", ondelete="CASCADE"), nullable=False)
    produto_id = mapped_column(Integer, ForeignKey("catalogo_produtos.id"), nullable=False)
    unidade_id = mapped_column(Integer, ForeignKey("unidades.id"), nullable=False)
    preco_base = mapped_column(Numeric(10, 2), nullable=True)  # opcional
    observacoes = mapped_column(Text, nullable=True)
    ativo = mapped_column(Boolean, default=True)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')
    updated_at = mapped_column(TIMESTAMP, server_default='NOW()', onupdate='NOW()')

    # Relacionamentos
    produtor = relationship("PerfilProdutor", back_populates="itens_producao")
    produto = relationship("CatalogoProduto", back_populates="itens_producao")
    unidade = relationship("Unidade", back_populates="itens_producao")
    periodos_capacidade = relationship("PeriodoCapacidade", back_populates="item_producao", cascade="all, delete-orphan")


class PeriodoCapacidade(Base):
    """Capacidade de produção por período (safra/mês/semana)"""
    __tablename__ = "periodos_capacidade"

    id = mapped_column(Integer, primary_key=True)
    item_producao_id = mapped_column(Integer, ForeignKey("itens_producao.id", ondelete="CASCADE"), nullable=False)
    tipo_periodo = mapped_column(String(50), nullable=False)  # week|month|custom
    periodo_inicio = mapped_column(Date, nullable=False)
    periodo_fim = mapped_column(Date, nullable=False)
    quantidade_capacidade = mapped_column(Numeric(10, 2), nullable=False)
    quantidade_previsao = mapped_column(Numeric(10, 2), nullable=True)  # opcional
    updated_by_user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')
    updated_at = mapped_column(TIMESTAMP, server_default='NOW()', onupdate='NOW()')

    # Relacionamentos
    item_producao = relationship("ItemProducao", back_populates="periodos_capacidade")
    updated_by_user = relationship("User", back_populates="periodos_capacidade_atualizados")
