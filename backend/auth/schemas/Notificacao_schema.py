# schemas/Notificacao_schema.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class NotificacaoBase(BaseModel):
    tipo: str
    titulo: str
    mensagem: str
    link_acao: Optional[str] = None


class NotificacaoCreate(NotificacaoBase):
    user_id: int


class NotificacaoUpdate(BaseModel):
    lida: bool = True


class NotificacaoResponse(NotificacaoBase):
    id: int
    user_id: int
    lida: bool
    created_at: datetime
    lida_em: Optional[datetime] = None

    class Config:
        from_attributes = True


class NotificacaoListResponse(BaseModel):
    """Lista de notificações com contadores"""
    total: int
    nao_lidas: int
    notificacoes: list[NotificacaoResponse]
