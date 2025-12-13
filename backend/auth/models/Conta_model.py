# models/Conta_model.py
from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base


class FornecedorIndividual(Base):
    __tablename__ = "fornecedores_individuais"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    cpf = mapped_column(String(14), nullable=False, unique=True)  # Format: XXX.XXX.XXX-XX
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relação com User
    user = relationship("User", backref="fornecedor_individual")


class GrupoInformal(Base):
    __tablename__ = "grupos_informais"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    cpfs = mapped_column(JSON, nullable=False)  # Lista de CPFs dos participantes
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relação com User
    user = relationship("User", backref="grupo_informal")


class GrupoFormal(Base):
    __tablename__ = "grupos_formais"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    cnpj = mapped_column(String(18), nullable=False, unique=True)  # Format: XX.XXX.XXX/XXXX-XX
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relação com User
    user = relationship("User", backref="grupo_formal")
