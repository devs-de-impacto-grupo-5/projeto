# models/Match_model.py
from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, JSON, Numeric, Date
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base


class ExecucaoMatch(Base):
    """Execução do motor de match para uma demanda"""
    __tablename__ = "execucoes_match"

    id = mapped_column(Integer, primary_key=True)
    versao_demanda_id = mapped_column(Integer, ForeignKey("versoes_demanda.id"), nullable=False)
    tipo_execucao = mapped_column(String(50), default='auto', nullable=False)  # auto|manual_trigger
    status = mapped_column(String(50), default='running', nullable=False)  # running|completed|failed
    parametros_json = mapped_column(JSON, nullable=True)  # pesos, regras
    iniciada_em = mapped_column(TIMESTAMP, server_default='NOW()')
    finalizada_em = mapped_column(TIMESTAMP, nullable=True)
    criada_por_user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=True)

    # Relacionamentos
    versao_demanda = relationship("VersaoDemanda", backref="execucoes_match")
    criada_por_user = relationship("User", backref="execucoes_match_criadas")
    candidatos = relationship("CandidatoMatch", back_populates="execucao_match", cascade="all, delete-orphan")
    grupos_fornecedores = relationship("GrupoFornecedor", back_populates="criado_de_match")


class CandidatoMatch(Base):
    """Candidatos gerados pelo motor de match (individual ou grupo)"""
    __tablename__ = "candidatos_match"

    id = mapped_column(Integer, primary_key=True)
    execucao_match_id = mapped_column(Integer, ForeignKey("execucoes_match.id", ondelete="CASCADE"), nullable=False)
    tipo_candidato = mapped_column(String(50), nullable=False)  # single|group
    score_total = mapped_column(Numeric(10, 2), nullable=False)
    explicacao_json = mapped_column(JSON, nullable=True)  # por quê recomendado
    percentual_cobertura = mapped_column(Numeric(5, 2), nullable=True)  # % dos itens cobertos
    status = mapped_column(String(50), default='active', nullable=False)  # active|superseded|rejected
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relacionamentos
    execucao_match = relationship("ExecucaoMatch", back_populates="candidatos")


class GrupoFornecedor(Base):
    """Grupo de fornecedores formado para atender uma demanda específica"""
    __tablename__ = "grupos_fornecedores"

    id = mapped_column(Integer, primary_key=True)
    versao_demanda_id = mapped_column(Integer, ForeignKey("versoes_demanda.id"), nullable=False)
    criado_de_match_id = mapped_column(Integer, ForeignKey("execucoes_match.id"), nullable=True)
    status = mapped_column(String(50), default='forming', nullable=False)  # forming|validated|submitted|won|lost|cancelled
    nome_grupo = mapped_column(String(255), nullable=True)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')
    updated_at = mapped_column(TIMESTAMP, server_default='NOW()', onupdate='NOW()')

    # Relacionamentos
    versao_demanda = relationship("VersaoDemanda", backref="grupos_fornecedores")
    criado_de_match = relationship("ExecucaoMatch", back_populates="grupos_fornecedores")
    membros = relationship("MembroGrupo", back_populates="grupo", cascade="all, delete-orphan")
    alocacoes = relationship("AlocacaoGrupo", back_populates="grupo", cascade="all, delete-orphan")
    propostas = relationship("Proposta", back_populates="grupo")


class MembroGrupo(Base):
    """Membros (produtores) de um grupo fornecedor"""
    __tablename__ = "membros_grupos"

    id = mapped_column(Integer, primary_key=True)
    grupo_id = mapped_column(Integer, ForeignKey("grupos_fornecedores.id", ondelete="CASCADE"), nullable=False)
    produtor_id = mapped_column(Integer, ForeignKey("perfis_produtores.id"), nullable=False)
    papel = mapped_column(String(50), default='member', nullable=False)  # member|leader
    ingressou_em = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relacionamentos
    grupo = relationship("GrupoFornecedor", back_populates="membros")
    produtor = relationship("PerfilProdutor", back_populates="grupos_fornecedores_membros")


class AlocacaoGrupo(Base):
    """Alocação de itens/quantidade a um produtor dentro de um grupo"""
    __tablename__ = "alocacoes_grupos"

    id = mapped_column(Integer, primary_key=True)
    grupo_id = mapped_column(Integer, ForeignKey("grupos_fornecedores.id", ondelete="CASCADE"), nullable=False)
    item_demanda_id = mapped_column(Integer, ForeignKey("itens_demanda.id"), nullable=False)
    produtor_id = mapped_column(Integer, ForeignKey("perfis_produtores.id"), nullable=False)
    quantidade_alocada = mapped_column(Numeric(10, 2), nullable=False)
    unidade_id = mapped_column(Integer, ForeignKey("unidades.id"), nullable=False)
    preco = mapped_column(Numeric(10, 2), nullable=True)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relacionamentos
    grupo = relationship("GrupoFornecedor", back_populates="alocacoes")
    item_demanda = relationship("ItemDemanda", back_populates="alocacoes_grupos")
    produtor = relationship("PerfilProdutor", backref="alocacoes_grupos")
    produto = relationship("CatalogoProduto", back_populates="alocacoes_grupos")
    unidade = relationship("Unidade", back_populates="alocacoes_grupos")
