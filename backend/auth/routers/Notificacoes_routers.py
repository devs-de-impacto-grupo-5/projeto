# routers/Notificacoes_routers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from schemas.Notificacao_schema import (
    NotificacaoCreate,
    NotificacaoUpdate,
    NotificacaoResponse,
    NotificacaoListResponse
)
from models.Notificacao_model import Notificacao
from models.User_model import User
from security.security import get_current_user, get_db

router = APIRouter(tags=["Notificações"], prefix="/notificacoes")


@router.post("", status_code=status.HTTP_201_CREATED, response_model=NotificacaoResponse)
async def criar_notificacao(
    notificacao_data: NotificacaoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cria uma nova notificação para um usuário"""
    notificacao = Notificacao(**notificacao_data.dict())
    db.add(notificacao)
    db.commit()
    db.refresh(notificacao)
    return notificacao


@router.get("/minhas", response_model=NotificacaoListResponse)
async def listar_minhas_notificacoes(
    apenas_nao_lidas: bool = False,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista notificações do usuário atual"""
    query = db.query(Notificacao).filter(Notificacao.user_id == current_user.id)

    if apenas_nao_lidas:
        query = query.filter(Notificacao.lida == False)

    notificacoes = query.order_by(Notificacao.created_at.desc()).limit(limit).all()

    total = db.query(Notificacao).filter(Notificacao.user_id == current_user.id).count()
    nao_lidas = db.query(Notificacao).filter(
        Notificacao.user_id == current_user.id,
        Notificacao.lida == False
    ).count()

    return NotificacaoListResponse(
        total=total,
        nao_lidas=nao_lidas,
        notificacoes=notificacoes
    )


@router.patch("/{notificacao_id}", response_model=NotificacaoResponse)
async def marcar_como_lida(
    notificacao_id: int,
    notificacao_update: NotificacaoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Marca notificação como lida"""
    notificacao = db.query(Notificacao).filter(
        Notificacao.id == notificacao_id,
        Notificacao.user_id == current_user.id
    ).first()

    if not notificacao:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")

    notificacao.lida = notificacao_update.lida
    if notificacao_update.lida:
        notificacao.lida_em = datetime.utcnow()

    db.commit()
    db.refresh(notificacao)

    return notificacao


@router.post("/marcar-todas-lidas", status_code=status.HTTP_200_OK)
async def marcar_todas_como_lidas(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Marca todas as notificações do usuário como lidas"""
    db.query(Notificacao).filter(
        Notificacao.user_id == current_user.id,
        Notificacao.lida == False
    ).update({"lida": True, "lida_em": datetime.utcnow()})

    db.commit()

    return {"message": "Todas as notificações foram marcadas como lidas"}
