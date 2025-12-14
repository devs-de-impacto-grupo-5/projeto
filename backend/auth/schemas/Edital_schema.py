from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class EditalItemPreview(BaseModel):
    produto_nome: Optional[str] = None
    descricao_adicional: Optional[str] = None
    quantidade: Optional[str] = None
    unidade: Optional[str] = None
    categoria: Optional[str] = None
    preco_estimado: Optional[str] = None
    confianca: Optional[str] = None


class EditalPreview(BaseModel):
    titulo: Optional[str] = None
    contexto: Optional[str] = None
    resumo: Optional[str] = None
    itens_preview: List[EditalItemPreview] = Field(default_factory=list)


class ArquivoProcessado(BaseModel):
    nome_original: Optional[str] = None
    caminho: Optional[str] = None
    tamanho_bytes: Optional[int] = None


class UsuarioProcessamento(BaseModel):
    id: Optional[int] = None
    nome: Optional[str] = None
    email: Optional[str] = None


class EditalProcessamentoResponse(BaseModel):
    success: bool = True
    rascunho_id: Optional[str] = None
    confianca_geral: Optional[str] = None
    num_itens: int = 0
    organization_id: Optional[int] = None
    preview: EditalPreview = Field(default_factory=EditalPreview)
    dados_extraidos: Dict[str, Any] = Field(default_factory=dict)
    arquivo_processado: Optional[ArquivoProcessado] = None
    processado_por: Optional[UsuarioProcessamento] = None
