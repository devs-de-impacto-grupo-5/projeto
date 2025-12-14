from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Text, JSON, Numeric
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base


class RascunhoEdital(Base):
    """Rascunho gerado a partir de upload e análise por IA"""
    __tablename__ = "rascunhos_editais"

    id = mapped_column(Integer, primary_key=True)
    titulo = mapped_column(String(500), nullable=True)
    descricao = mapped_column(Text, nullable=True)
    organizacao_id = mapped_column(Integer, ForeignKey("organizacoes.id"), nullable=True)
    arquivo_id = mapped_column(Integer, ForeignKey("arquivos.id"), nullable=True)
    criada_por_user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    conteudo_estruturado_json = mapped_column(JSON, nullable=True)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')
    updated_at = mapped_column(TIMESTAMP, server_default='NOW()', onupdate='NOW()')

    # Relacionamentos
    arquivo = relationship("Arquivo", backref="rascunhos")
    criada_por_user = relationship("User", backref="rascunhos_criados")
    itens = relationship("ItemRascunho", back_populates="rascunho", cascade="all, delete-orphan")


class ItemRascunho(Base):
    """Itens extraídos e associados ao rascunho"""
    __tablename__ = "itens_rascunho"

    id = mapped_column(Integer, primary_key=True)
    rascunho_id = mapped_column(Integer, ForeignKey("rascunhos_editais.id", ondelete="CASCADE"), nullable=False)
    produto_nome = mapped_column(String(500), nullable=True)
    descricao_adicional = mapped_column(Text, nullable=True)
    quantidade = mapped_column(String(100), nullable=True)
    unidade = mapped_column(String(100), nullable=True)
    categoria = mapped_column(String(255), nullable=True)
    preco_estimado = mapped_column(Numeric(12, 2), nullable=True)
    confianca = mapped_column(String(50), nullable=True)

    # Relacionamentos
    rascunho = relationship("RascunhoEdital", back_populates="itens")
