# schemas/Proposta_schema.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class ItemPropostaBase(BaseModel):
    item_demanda_id: int
    produto_id: int
    unidade_id: int
    quantidade: Decimal
    preco: Optional[Decimal] = None
    substituto_de_produto_id: Optional[int] = None
    motivo_substituicao: Optional[str] = None
    flag_aviso: bool = False


class ItemPropostaCreate(ItemPropostaBase):
    pass


class ItemPropostaResponse(ItemPropostaBase):
    id: int
    proposta_id: int
    produto_nome: Optional[str] = None
    unidade_nome: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PropostaBase(BaseModel):
    versao_demanda_id: int
    organizacao_id: int
    tipo_proposta: str = Field(..., pattern="^(single|group)$")
    produtor_id: Optional[int] = None
    grupo_id: Optional[int] = None
    valor_total: Optional[Decimal] = None


class PropostaCreate(PropostaBase):
    itens: List[ItemPropostaCreate]


class PropostaUpdate(BaseModel):
    status: Optional[str] = None
    valor_total: Optional[Decimal] = None


class PropostaResponse(PropostaBase):
    id: int
    status: str
    criada_por_user_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    itens: List[ItemPropostaResponse] = []

    class Config:
        from_attributes = True


class ConfirmacaoParticipanteBase(BaseModel):
    proposta_id: int
    produtor_id: int
    status: str = "invited"
    motivo_recusa: Optional[str] = None


class ConfirmacaoParticipanteCreate(ConfirmacaoParticipanteBase):
    pass


class ConfirmacaoParticipanteUpdate(BaseModel):
    status: str = Field(..., pattern="^(accepted|declined)$")
    motivo_recusa: Optional[str] = None


class ConfirmacaoParticipanteResponse(ConfirmacaoParticipanteBase):
    id: int
    convidado_em: datetime
    respondido_em: Optional[datetime] = None
    expira_em: Optional[datetime] = None
    produtor_nome: Optional[str] = None

    class Config:
        from_attributes = True


class SubmissaoPropostaBase(BaseModel):
    tipo_submissao: str = Field(..., pattern="^(digital|physical)$")
    observacoes: Optional[str] = None


class SubmissaoPropostaCreate(SubmissaoPropostaBase):
    proposta_id: int


class SubmissaoPropostaUpdate(BaseModel):
    status: Optional[str] = None
    observacoes: Optional[str] = None


class EtapaSubmissaoFisicaBase(BaseModel):
    numero_etapa: int
    titulo: str
    descricao: Optional[str] = None
    status: str = "todo"


class EtapaSubmissaoFisicaUpdate(BaseModel):
    status: str = Field(..., pattern="^(done|skipped)$")


class EtapaSubmissaoFisicaResponse(EtapaSubmissaoFisicaBase):
    id: int
    submissao_proposta_id: int
    arquivo_evidencia_id: Optional[int] = None
    concluida_em: Optional[datetime] = None

    class Config:
        from_attributes = True


class SubmissaoPropostaResponse(SubmissaoPropostaBase):
    id: int
    proposta_id: int
    status: str
    submetida_em: Optional[datetime] = None
    arquivo_comprovante_id: Optional[int] = None
    etapas_fisica: List[EtapaSubmissaoFisicaResponse] = []

    class Config:
        from_attributes = True
