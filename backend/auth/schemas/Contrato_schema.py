# schemas/Contrato_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ModeloContratoBase(BaseModel):
    organizacao_id: int
    nome: str
    numero_versao: int
    arquivo_template_id: int
    ativo: bool = True


class ModeloContratoCreate(ModeloContratoBase):
    pass


class ModeloContratoResponse(ModeloContratoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ContratoBase(BaseModel):
    organizacao_id: int
    demanda_id: int
    proposta_id: int
    modelo_id: Optional[int] = None


class ContratoCreate(ContratoBase):
    pass


class ContratoUpdate(BaseModel):
    status: Optional[str] = None
    arquivo_contrato_id: Optional[int] = None


class ContratoResponse(ContratoBase):
    id: int
    status: str
    arquivo_contrato_id: Optional[int] = None
    gerado_em: Optional[datetime] = None
    assinado_em: Optional[datetime] = None
    organizacao_nome: Optional[str] = None
    demanda_titulo: Optional[str] = None
    blockchain_registrado: bool = False
    blockchain_transaction_hash: Optional[str] = None

    class Config:
        from_attributes = True


class RegistroBlockchainBase(BaseModel):
    contrato_id: int
    hash_documento: str
    blockchain_network: str
    wallet_address: Optional[str] = None


class RegistroBlockchainCreate(RegistroBlockchainBase):
    pass


class RegistroBlockchainUpdate(BaseModel):
    transaction_hash: Optional[str] = None
    block_number: Optional[int] = None
    status: Optional[str] = None
    erro_mensagem: Optional[str] = None


class RegistroBlockchainResponse(RegistroBlockchainBase):
    id: int
    transaction_hash: Optional[str] = None
    block_number: Optional[int] = None
    status: str
    metadados_json: Optional[dict] = None
    erro_mensagem: Optional[str] = None
    registrado_em: Optional[datetime] = None
    verificado_em: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
