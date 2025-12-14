# schemas/Documento_schema.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TipoDocumentoBase(BaseModel):
    codigo: str
    nome: str
    descricao: Optional[str] = None
    validade_dias: Optional[int] = None


class TipoDocumentoResponse(TipoDocumentoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DocumentoProdutorBase(BaseModel):
    produtor_id: int
    tipo_documento_id: int


class DocumentoProdutorCreate(DocumentoProdutorBase):
    pass


class DocumentoProdutorUpdate(BaseModel):
    status: Optional[str] = Field(None, pattern="^(submitted|in_review|approved|rejected|expired)$")
    rejection_reason: Optional[str] = None


class DocumentoProdutorResponse(DocumentoProdutorBase):
    id: int
    status: str
    reviewed_by_user_id: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    tipo_documento_nome: Optional[str] = None
    tipo_documento_codigo: Optional[str] = None

    class Config:
        from_attributes = True


class ArquivoDocumentoBase(BaseModel):
    documento_produtor_id: int
    arquivo_id: int
    versao: int


class ArquivoDocumentoResponse(ArquivoDocumentoBase):
    id: int
    uploaded_by_user_id: Optional[int] = None
    uploaded_at: datetime
    arquivo_nome: Optional[str] = None

    class Config:
        from_attributes = True


class WorkflowDocumentoBase(BaseModel):
    produtor_id: int
    tipo_documento_id: int


class WorkflowDocumentoCreate(WorkflowDocumentoBase):
    pass


class WorkflowDocumentoUpdate(BaseModel):
    status: Optional[str] = Field(None, pattern="^(in_progress|done|cancelled)$")
    etapa_atual: Optional[int] = None


class EtapaWorkflowBase(BaseModel):
    numero_etapa: int
    titulo: str
    descricao: Optional[str] = None
    status: str = "todo"


class EtapaWorkflowUpdate(BaseModel):
    status: str = Field(..., pattern="^(done|skipped)$")


class EtapaWorkflowResponse(EtapaWorkflowBase):
    id: int
    workflow_id: int
    arquivo_evidencia_id: Optional[int] = None
    concluida_em: Optional[datetime] = None

    class Config:
        from_attributes = True


class WorkflowDocumentoResponse(WorkflowDocumentoBase):
    id: int
    status: str
    etapa_atual: int
    created_at: datetime
    updated_at: datetime
    tipo_documento_nome: Optional[str] = None
    etapas: List[EtapaWorkflowResponse] = []

    class Config:
        from_attributes = True


class DocumentoChecklistItem(BaseModel):
    """Item do checklist de documentos do produtor"""
    tipo_documento_id: int
    tipo_documento_codigo: str
    tipo_documento_nome: str
    obrigatorio: bool
    status: str  # pending|submitted|in_review|approved|rejected|expired
    documento_id: Optional[int] = None
    expires_at: Optional[datetime] = None


class DocumentoChecklistResponse(BaseModel):
    """Checklist completo de documentos do produtor"""
    produtor_id: int
    total_documentos: int
    documentos_pendentes: int
    documentos_aprovados: int
    documentos_em_analise: int
    documentos_reprovados: int
    perfil_completo: bool
    itens: List[DocumentoChecklistItem]
