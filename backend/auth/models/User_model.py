# models/User_model.py
from sqlalchemy import Integer, String, TIMESTAMP, Float
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base  # Importação direta da Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255), nullable=False)
    email = mapped_column(String(255), unique=True, nullable=False)
    senha = mapped_column(String(255), nullable=False)

    # Tipo de usuário: "entidade_executora" ou "produtor"
    tipo_usuario = mapped_column(String(50), nullable=False)

    # Subtipo específico:
    # Se tipo_usuario="entidade_executora": "escola" ou "governo"
    # Se tipo_usuario="produtor": "fornecedor_individual", "grupo_informal" ou "grupo_formal"
    subtipo_usuario = mapped_column(String(50), nullable=False)

    # Localização (coordenadas GPS)
    latitude = mapped_column(Float, nullable=True)
    longitude = mapped_column(Float, nullable=True)

    role = mapped_column(String(100), nullable=True)  # Kept for backward compatibility

    # Novos campos para MVP
    status = mapped_column(String(50), default='active', nullable=False)  # active|disabled|pending_verification
    phone = mapped_column(String(20), nullable=True)
    last_login_at = mapped_column(TIMESTAMP, nullable=True)

    created_at = mapped_column(TIMESTAMP, server_default='NOW()')
    updated_at = mapped_column(TIMESTAMP, server_default='NOW()', onupdate='NOW()')

    # Relacionamentos explícitos para back_populates
    escola = relationship("Escola", back_populates="user", uselist=False)
    governo = relationship("Governo", back_populates="user", uselist=False)
    produtos = relationship("Produto", back_populates="user")
    fornecedor_individual = relationship("FornecedorIndividual", back_populates="user", uselist=False)
    grupo_informal = relationship("GrupoInformal", back_populates="user", uselist=False)
    grupo_formal = relationship("GrupoFormal", back_populates="user", uselist=False)
    perfil_produtor = relationship("PerfilProdutor", back_populates="user", uselist=False)
    documentos = relationship("DocumentoUsuario", back_populates="user", cascade="all, delete-orphan")
    substituicoes_aprovadas = relationship("SubstitucaoEquivalencia", back_populates="aprovado_por")
    decisoes_propostas = relationship("DecisaoProposta", back_populates="decidida_por_user")
    demandas_criadas = relationship("Demanda", back_populates="criada_por_user")
    versoes_demanda_criadas = relationship("VersaoDemanda", back_populates="criada_por_user")
    propostas_criadas = relationship("Proposta", back_populates="criada_por_user")
    execucoes_match_criadas = relationship("ExecucaoMatch", back_populates="criada_por_user")
    documentos_revisados = relationship("DocumentoProdutor", back_populates="reviewed_by_user")
    uploads_documentos = relationship("ArquivoDocumento", back_populates="uploaded_by_user")
    arquivos_uploadados = relationship("Arquivo", back_populates="uploaded_by_user")
    periodos_capacidade_atualizados = relationship("PeriodoCapacidade", back_populates="updated_by_user")
    eventos_auditoria = relationship("EventoAuditoria", back_populates="user")
    notificacoes = relationship("Notificacao", back_populates="user")
    usuario_governo = relationship("UsuarioGoverno", back_populates="user", uselist=False)

    def __init__(self, **kwargs):
        if 'senha' in kwargs:
            senha_plana = kwargs.pop('senha')
            self.senha = pwd_context.hash(senha_plana)
        super().__init__(**kwargs)

    def verify_password(self, senha_plana):
        return pwd_context.verify(senha_plana, self.senha)
