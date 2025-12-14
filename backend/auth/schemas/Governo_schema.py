# schemas/Governo_schema.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal


class OrganizacaoBase(BaseModel):
    tipo: str = Field(..., pattern="^(municipality|school|secretariat|other)$")
    nome: str
    identificacao_legal: Optional[str] = None
    endereco_json: Optional[Dict[str, Any]] = None


class OrganizacaoCreate(OrganizacaoBase):
    pass


class OrganizacaoUpdate(BaseModel):
    nome: Optional[str] = None
    identificacao_legal: Optional[str] = None
    endereco_json: Optional[Dict[str, Any]] = None
    status: Optional[str] = Field(None, pattern="^(active|inactive)$")


class OrganizacaoResponse(OrganizacaoBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    total_usuarios: Optional[int] = 0
    total_demandas: Optional[int] = 0

    class Config:
        from_attributes = True


class UsuarioGovernoBase(BaseModel):
    user_id: int
    organizacao_id: int
    cargo: Optional[str] = None
    permissoes_json: Optional[Dict[str, Any]] = None


class UsuarioGovernoCreate(UsuarioGovernoBase):
    pass


class UsuarioGovernoUpdate(BaseModel):
    cargo: Optional[str] = None
    permissoes_json: Optional[Dict[str, Any]] = None
    ativo: Optional[str] = None


class UsuarioGovernoResponse(UsuarioGovernoBase):
    id: int
    ativo: str
    created_at: datetime
    updated_at: datetime
    user_nome: Optional[str] = None
    user_email: Optional[str] = None
    organizacao_nome: Optional[str] = None

    class Config:
        from_attributes = True


class DecisaoPropostaBase(BaseModel):
    proposta_id: int
    decisao: str = Field(..., pattern="^(selected|rejected)$")
    justificativa: Optional[str] = None


class DecisaoPropostaCreate(DecisaoPropostaBase):
    pass


class DecisaoPropostaResponse(DecisaoPropostaBase):
    id: int
    decidida_por_user_id: int
    decidida_por_nome: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardGovernoStats(BaseModel):
    """Estatísticas do dashboard do governo"""
    demandas_abertas: int
    demandas_publicadas: int
    propostas_recebidas: int
    propostas_pendentes_avaliacao: int
    contratos_ativos: int
    itens_sem_cobertura: int
    prazos_criticos: int


class ItemSemCobertura(BaseModel):
    """Item de demanda sem cobertura suficiente"""
    demanda_id: int
    demanda_titulo: str
    item_id: int
    produto_nome: str
    quantidade_demandada: Decimal
    quantidade_coberta: Decimal
    percentual_cobertura: float


class PrazoCritico(BaseModel):
    """Demanda com prazo crítico"""
    demanda_id: int
    demanda_titulo: str
    encerra_em: datetime
    dias_restantes: int
    propostas_recebidas: int


class DashboardGovernoResponse(BaseModel):
    """Dashboard completo do governo"""
    stats: DashboardGovernoStats
    itens_sem_cobertura: List[ItemSemCobertura]
    prazos_criticos: List[PrazoCritico]
    ultimas_propostas: List[Dict[str, Any]]
