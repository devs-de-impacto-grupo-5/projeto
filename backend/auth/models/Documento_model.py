# models/Documento_model.py
from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Text, JSON, BigInteger
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base


class TipoDocumento(Base):
    """Tipos de documentos requeridos"""
    __tablename__ = "tipos_documentos"

    id = mapped_column(Integer, primary_key=True)
    codigo = mapped_column(String(50), unique=True, nullable=False)  # "DAP", "CPF", "CNPJ", etc
    nome = mapped_column(String(255), nullable=False)
    descricao = mapped_column(Text, nullable=True)
    requerido_para_json = mapped_column(JSON, nullable=True)  # {tipo_produtor: [...], tipo_edital: [...]}
    validade_dias = mapped_column(Integer, nullable=True)  # NULL = não expira
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')
    updated_at = mapped_column(TIMESTAMP, server_default='NOW()', onupdate='NOW()')

    # Relacionamentos
    documentos_produtor = relationship("DocumentoProdutor", back_populates="tipo_documento")
    workflows_documentos = relationship("WorkflowDocumento", back_populates="tipo_documento")
    requisitos_demanda = relationship("RequisitoDemanda", back_populates="tipo_documento")


class Arquivo(Base):
    """Armazenamento de arquivos com versionamento"""
    __tablename__ = "arquivos"

    id = mapped_column(Integer, primary_key=True)
    nome_original = mapped_column(String(500), nullable=False)
    caminho_storage = mapped_column(String(500), nullable=False)
    mime_type = mapped_column(String(100), nullable=True)
    tamanho_bytes = mapped_column(BigInteger, nullable=True)
    hash_arquivo = mapped_column(String(255), nullable=True)  # SHA256
    uploaded_by_user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    uploaded_at = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relacionamentos
    uploaded_by_user = relationship("User", back_populates="arquivos_uploadados")
    arquivos_documentos = relationship("ArquivoDocumento", back_populates="arquivo", cascade="all, delete-orphan")
    versoes_demanda = relationship("VersaoDemanda", back_populates="arquivo_original")
    etapas_workflows = relationship("EtapaWorkflow", back_populates="arquivo_evidencia")
    etapas_submissao_fisica = relationship("EtapaSubmissaoFisica", back_populates="arquivo_evidencia")
    submissoes_propostas = relationship("SubmissaoProposta", back_populates="arquivo_comprovante")
    modelos_contrato = relationship("ModeloContrato", back_populates="arquivo_template")
    contratos = relationship("Contrato", back_populates="arquivo_contrato")


class DocumentoProdutor(Base):
    """Documentos específicos do produtor (versionável)"""
    __tablename__ = "documentos_produtor"

    id = mapped_column(Integer, primary_key=True)
    produtor_id = mapped_column(Integer, ForeignKey("perfis_produtores.id", ondelete="CASCADE"), nullable=False)
    tipo_documento_id = mapped_column(Integer, ForeignKey("tipos_documentos.id"), nullable=False)
    status = mapped_column(String(50), default='pending', nullable=False)  # pending|submitted|in_review|approved|rejected|expired
    reviewed_by_user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_at = mapped_column(TIMESTAMP, nullable=True)
    rejection_reason = mapped_column(Text, nullable=True)
    expires_at = mapped_column(TIMESTAMP, nullable=True)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')
    updated_at = mapped_column(TIMESTAMP, server_default='NOW()', onupdate='NOW()')

    # Relacionamentos
    produtor = relationship("PerfilProdutor", back_populates="documentos_produtor")
    tipo_documento = relationship("TipoDocumento", back_populates="documentos_produtor")
    reviewed_by_user = relationship("User", back_populates="documentos_revisados")
    arquivos = relationship("ArquivoDocumento", back_populates="documento", cascade="all, delete-orphan")


class ArquivoDocumento(Base):
    """Versionamento de arquivos de documentos"""
    __tablename__ = "arquivos_documentos"

    id = mapped_column(Integer, primary_key=True)
    documento_produtor_id = mapped_column(Integer, ForeignKey("documentos_produtor.id", ondelete="CASCADE"), nullable=False)
    arquivo_id = mapped_column(Integer, ForeignKey("arquivos.id"), nullable=False)
    versao = mapped_column(Integer, nullable=False)
    uploaded_by_user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    uploaded_at = mapped_column(TIMESTAMP, server_default='NOW()')

    # Relacionamentos
    documento = relationship("DocumentoProdutor", back_populates="arquivos")
    arquivo = relationship("Arquivo", back_populates="arquivos_documentos")
    uploaded_by_user = relationship("User", back_populates="uploads_documentos")


class WorkflowDocumento(Base):
    """Workflow de emissão assistida de documentos"""
    __tablename__ = "workflows_documentos"

    id = mapped_column(Integer, primary_key=True)
    produtor_id = mapped_column(Integer, ForeignKey("perfis_produtores.id", ondelete="CASCADE"), nullable=False)
    tipo_documento_id = mapped_column(Integer, ForeignKey("tipos_documentos.id"), nullable=False)
    status = mapped_column(String(50), default='not_started', nullable=False)  # not_started|in_progress|done|cancelled
    etapa_atual = mapped_column(Integer, default=1)
    created_at = mapped_column(TIMESTAMP, server_default='NOW()')
    updated_at = mapped_column(TIMESTAMP, server_default='NOW()', onupdate='NOW()')

    # Relacionamentos
    produtor = relationship("PerfilProdutor", back_populates="workflows_documentos")
    tipo_documento = relationship("TipoDocumento", back_populates="workflows_documentos")
    etapas = relationship("EtapaWorkflow", back_populates="workflow", cascade="all, delete-orphan")


class EtapaWorkflow(Base):
    """Etapas de um workflow de documento"""
    __tablename__ = "etapas_workflows"

    id = mapped_column(Integer, primary_key=True)
    workflow_id = mapped_column(Integer, ForeignKey("workflows_documentos.id", ondelete="CASCADE"), nullable=False)
    numero_etapa = mapped_column(Integer, nullable=False)
    titulo = mapped_column(String(255), nullable=False)
    descricao = mapped_column(Text, nullable=True)
    status = mapped_column(String(50), default='todo', nullable=False)  # todo|done|skipped
    arquivo_evidencia_id = mapped_column(Integer, ForeignKey("arquivos.id"), nullable=True)
    concluida_em = mapped_column(TIMESTAMP, nullable=True)

    # Relacionamentos
    workflow = relationship("WorkflowDocumento", back_populates="etapas")
    arquivo_evidencia = relationship("Arquivo", back_populates="etapas_workflows")
