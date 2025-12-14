# schemas/Admin_schema.py
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class ConfiguracaoMatchBase(BaseModel):
    """Configuração dos pesos do motor de match"""
    peso_produto: float = Field(0.28, ge=0, le=1)
    peso_capacidade: float = Field(0.22, ge=0, le=1)
    peso_historico: float = Field(0.18, ge=0, le=1)
    peso_proximidade: float = Field(0.12, ge=0, le=1)
    peso_tempo_resposta: float = Field(0.10, ge=0, le=1)
    peso_certificacoes: float = Field(0.10, ge=0, le=1)
    regras_adicionais: Optional[Dict[str, Any]] = None


class ConfiguracaoMatchResponse(ConfiguracaoMatchBase):
    versao: int
    ativa: bool
    criada_por_user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class SubstituicaoEquivalenciaBase(BaseModel):
    from_product_id: int
    to_product_id: int
    razao_equivalencia: Optional[str] = None
    observacoes: Optional[str] = None
    ativo: bool = True


class SubstituicaoEquivalenciaCreate(SubstituicaoEquivalenciaBase):
    pass


class SubstituicaoEquivalenciaUpdate(BaseModel):
    razao_equivalencia: Optional[str] = None
    observacoes: Optional[str] = None
    ativo: Optional[bool] = None


class SubstituicaoEquivalenciaResponse(SubstituicaoEquivalenciaBase):
    id: int
    aprovado_por_user_id: int
    aprovado_por_nome: Optional[str] = None
    produto_origem_nome: Optional[str] = None
    produto_destino_nome: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UsuarioAdminBase(BaseModel):
    user_id: int
    nome: str
    email: str
    tipo_usuario: str
    subtipo_usuario: str
    status: str


class UsuarioAdminUpdate(BaseModel):
    status: Optional[str] = Field(None, pattern="^(active|disabled|pending_verification)$")
    role: Optional[str] = None


class UsuarioAdminResponse(UsuarioAdminBase):
    id: int
    created_at: datetime
    last_login_at: Optional[datetime] = None
    total_demandas: Optional[int] = 0
    total_propostas: Optional[int] = 0

    class Config:
        from_attributes = True


class EventoAuditoriaResponse(BaseModel):
    """Evento de auditoria"""
    id: int
    user_id: Optional[int] = None
    user_nome: Optional[str] = None
    acao: str
    entidade_tipo: str
    entidade_id: Optional[int] = None
    detalhes: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class RelatorioSistemaResponse(BaseModel):
    """Relatório geral do sistema"""
    total_usuarios: int
    total_produtores: int
    total_governo: int
    total_organizacoes: int
    total_demandas: int
    total_propostas: int
    total_contratos: int
    total_produtos_catalogo: int
    usuarios_ativos_ultimos_30_dias: int
    demandas_publicadas_ultimos_30_dias: int
    propostas_criadas_ultimos_30_dias: int
    contratos_assinados_ultimos_30_dias: int
