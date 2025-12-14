# models/Catalogo_model.py
from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base


class Unidade(Base):
    """Unidades de medida padronizadas"""
    __tablename__ = "unidades"

    id = mapped_column(Integer, primary_key=True)
    codigo = mapped_column(String(20), unique=True, nullable=False)  # kg, litro, unidade, cx
    nome = mapped_column(String(100), nullable=False)
    tipo = mapped_column(String(50), nullable=False)  # mass|volume|count|other

    # Relacionamentos
    catalogo_produtos = relationship("CatalogoProduto", back_populates="unidade_padrao")
    itens_producao = relationship("ItemProducao", back_populates="unidade")
    itens_demanda = relationship("ItemDemanda", back_populates="unidade")
    itens_proposta = relationship("ItemProposta", back_populates="unidade")
    alocacoes_grupos = relationship("AlocacaoGrupo", back_populates="unidade")


class CatalogoProduto(Base):
    """Catálogo padronizado de produtos"""
    __tablename__ = "catalogo_produtos"

    id = mapped_column(Integer, primary_key=True)
    nome = mapped_column(String(255), nullable=False)
    categoria = mapped_column(String(100), nullable=False)  # hortifruti|graos|laticinios|processados|outros
    unidade_padrao_id = mapped_column(Integer, ForeignKey("unidades.id"), nullable=False)
    ativo = mapped_column(Boolean, default=True)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')
    updated_at = mapped_column(TIMESTAMP, server_default='NOW()', onupdate='NOW()')

    # Relacionamentos
    unidade_padrao = relationship("Unidade", back_populates="catalogo_produtos")
    sinonimos = relationship("SinonymoProduto", back_populates="produto", cascade="all, delete-orphan")
    itens_producao = relationship("ItemProducao", back_populates="produto")
    itens_demanda = relationship("ItemDemanda", back_populates="produto")
    itens_proposta = relationship(
        "ItemProposta",
        foreign_keys="ItemProposta.produto_id",
        back_populates="produto"
    )
    itens_proposta_substituto = relationship(
        "ItemProposta",
        foreign_keys="ItemProposta.substituto_de_produto_id",
        back_populates="produto_substituto"
    )
    equivalencias_origem = relationship("SubstitucaoEquivalencia", foreign_keys="SubstitucaoEquivalencia.from_product_id", back_populates="produto_origem")
    equivalencias_destino = relationship("SubstitucaoEquivalencia", foreign_keys="SubstitucaoEquivalencia.to_product_id", back_populates="produto_destino")


class SinonymoProduto(Base):
    """Sinônimos de produtos para busca"""
    __tablename__ = "sinonimos_produtos"

    id = mapped_column(Integer, primary_key=True)
    produto_id = mapped_column(Integer, ForeignKey("catalogo_produtos.id", ondelete="CASCADE"), nullable=False)
    sinonimo = mapped_column(String(255), nullable=False)

    # Relacionamentos
    produto = relationship("CatalogoProduto", back_populates="sinonimos")


class SubstitucaoEquivalencia(Base):
    """Equivalências de substituição entre produtos"""
    __tablename__ = "substituicoes_equivalencias"

    id = mapped_column(Integer, primary_key=True)
    from_product_id = mapped_column(Integer, ForeignKey("catalogo_produtos.id"), nullable=False)
    to_product_id = mapped_column(Integer, ForeignKey("catalogo_produtos.id"), nullable=False)
    razao_equivalencia = mapped_column(String(20), nullable=True)  # ex: "1kg", "1:1"
    observacoes = mapped_column(String(500), nullable=True)
    ativo = mapped_column(Boolean, default=True)
    aprovado_por_user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relacionamentos
    produto_origem = relationship("CatalogoProduto", foreign_keys=[from_product_id], back_populates="equivalencias_origem")
    produto_destino = relationship("CatalogoProduto", foreign_keys=[to_product_id], back_populates="equivalencias_destino")
    aprovado_por = relationship("User", back_populates="substituicoes_aprovadas")
