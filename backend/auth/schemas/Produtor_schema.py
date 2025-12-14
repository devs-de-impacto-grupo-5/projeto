# schemas/Produtor_schema.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal


class PerfilProdutorBase(BaseModel):
    tipo_produtor: str = Field(..., pattern="^(individual|cooperative|association|company)$")
    identificacao_legal: Optional[str] = None
    rg_ie: Optional[str] = None
    endereco_json: Optional[Dict[str, Any]] = None
    capacidades_entrega_json: Optional[List[str]] = None


class PerfilProdutorCreate(PerfilProdutorBase):
    user_id: int


class PerfilProdutorUpdate(BaseModel):
    tipo_produtor: Optional[str] = None
    identificacao_legal: Optional[str] = None
    rg_ie: Optional[str] = None
    endereco_json: Optional[Dict[str, Any]] = None
    capacidades_entrega_json: Optional[List[str]] = None
    status_perfil: Optional[str] = None


class PerfilProdutorResponse(PerfilProdutorBase):
    id: int
    user_id: int
    status_perfil: str
    created_at: datetime
    updated_at: datetime
    user_nome: Optional[str] = None
    user_email: Optional[str] = None

    class Config:
        from_attributes = True


class ItemProducaoBase(BaseModel):
    produto_id: int
    unidade_id: int
    preco_base: Optional[Decimal] = None
    ativo: bool = True


class ItemProducaoCreate(ItemProducaoBase):
    produtor_id: int


class ItemProducaoUpdate(BaseModel):
    preco_base: Optional[Decimal] = None
    ativo: Optional[bool] = None


class PeriodoCapacidadeBase(BaseModel):
    tipo_periodo: str = Field(..., pattern="^(monthly|weekly|seasonal|custom)$")
    periodo_inicio: Optional[date] = None
    periodo_fim: Optional[date] = None
    quantidade_capacidade: Optional[Decimal] = None
    quantidade_previsao: Optional[Decimal] = None


class PeriodoCapacidadeCreate(PeriodoCapacidadeBase):
    item_producao_id: int


class PeriodoCapacidadeUpdate(BaseModel):
    quantidade_capacidade: Optional[Decimal] = None
    quantidade_previsao: Optional[Decimal] = None


class PeriodoCapacidadeResponse(PeriodoCapacidadeBase):
    id: int
    item_producao_id: int
    updated_by_user_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ItemProducaoResponse(ItemProducaoBase):
    id: int
    produtor_id: int
    produto_nome: Optional[str] = None
    unidade_nome: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    periodos_capacidade: List[PeriodoCapacidadeResponse] = []

    class Config:
        from_attributes = True


class DashboardProdutorResponse(BaseModel):
    """Dashboard do produtor com informações consolidadas"""
    perfil_id: int
    perfil_completo: bool
    documentos_pendentes: int
    documentos_aprovados: int
    produtos_cadastrados: int
    demandas_disponiveis: int
    propostas_ativas: int
    propostas_aguardando_resposta: int
    contratos_ativos: int
    notificacoes_nao_lidas: int
    pendencias: List[Dict[str, Any]]
