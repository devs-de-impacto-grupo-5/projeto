# models/Conta_model.py
from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, JSON, Float, Text
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base


class Escola(Base):
    __tablename__ = "escolas"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    nome_escola = mapped_column(String(255), nullable=False)
    endereco = mapped_column(Text, nullable=True)
    telefone = mapped_column(String(20), nullable=True)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relação com User
    user = relationship("User", back_populates="escola")


class Governo(Base):
    __tablename__ = "governos"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    nome_orgao = mapped_column(String(255), nullable=False)
    nivel = mapped_column(String(50), nullable=False)  # "municipal", "estadual", "federal"
    endereco = mapped_column(Text, nullable=True)
    telefone = mapped_column(String(20), nullable=True)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relação com User
    user = relationship("User", back_populates="governo")


class Produto(Base):
    __tablename__ = "produtos"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    nome = mapped_column(String(255), nullable=False)
    descricao = mapped_column(Text, nullable=True)
    categoria = mapped_column(String(100), nullable=False)
    preco = mapped_column(Float, nullable=False)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')
    updated_at = mapped_column(TIMESTAMP, server_default='NOW()', onupdate='NOW()')

    # Relação com User
    user = relationship("User", back_populates="produtos")


class FornecedorIndividual(Base):
    __tablename__ = "fornecedores_individuais"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    cpf = mapped_column(String(14), nullable=False, unique=True)  # Format: XXX.XXX.XXX-XX
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relação com User
    user = relationship("User", back_populates="fornecedor_individual")


class GrupoInformal(Base):
    __tablename__ = "grupos_informais"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    # Armazena lista de participantes: [{"nome": "...", "cpf": "..."}, ...]
    participantes = mapped_column(JSON, nullable=False)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relação com User
    user = relationship("User", back_populates="grupo_informal")


class GrupoFormal(Base):
    __tablename__ = "grupos_formais"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    cnpj = mapped_column(String(18), nullable=False, unique=True)  # Format: XX.XXX.XXX/XXXX-XX
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relação com User
    user = relationship("User", back_populates="grupo_formal")
