# routers/Governo_routers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List
from datetime import datetime, timedelta
from decimal import Decimal

from schemas.Governo_schema import (
    OrganizacaoCreate,
    OrganizacaoUpdate,
    OrganizacaoResponse,
    UsuarioGovernoCreate,
    UsuarioGovernoUpdate,
    UsuarioGovernoResponse,
    DecisaoPropostaCreate,
    DecisaoPropostaResponse,
    DashboardGovernoResponse,
    DashboardGovernoStats,
    ItemSemCobertura,
    PrazoCritico
)
from models.Organizacao_model import Organizacao, UsuarioGoverno
from models.Contrato_model import DecisaoProposta
from models.Demanda_model import Demanda, VersaoDemanda, ItemDemanda
from models.Proposta_model import Proposta, ItemProposta
from models.Contrato_model import Contrato
from models.User_model import User
from security.security import get_current_user, get_db

router = APIRouter(tags=["Governo"], prefix="/governo")


# ===== ORGANIZAÇÕES (RF-03) =====

@router.post("/organizacoes", status_code=status.HTTP_201_CREATED, response_model=OrganizacaoResponse)
async def criar_organizacao(
    org_data: OrganizacaoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """RF-03: Multi-organização - Criar organização"""
    org = Organizacao(**org_data.dict())
    db.add(org)
    db.commit()
    db.refresh(org)
    return org


@router.get("/organizacoes", response_model=List[OrganizacaoResponse])
async def listar_organizacoes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista todas as organizações"""
    orgs = db.query(Organizacao).all()
    return orgs


@router.patch("/organizacoes/{org_id}", response_model=OrganizacaoResponse)
async def atualizar_organizacao(
    org_id: int,
    org_update: OrganizacaoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza organização"""
    org = db.query(Organizacao).filter(Organizacao.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organização não encontrada")

    for key, value in org_update.dict(exclude_unset=True).items():
        setattr(org, key, value)

    db.commit()
    db.refresh(org)
    return org


@router.post("/usuarios", status_code=status.HTTP_201_CREATED, response_model=UsuarioGovernoResponse)
async def associar_usuario_organizacao(
    usuario_data: UsuarioGovernoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """RF-03: Associa usuário do governo com organização"""
    usuario_gov = UsuarioGoverno(**usuario_data.dict())
    db.add(usuario_gov)
    db.commit()
    db.refresh(usuario_gov)
    return usuario_gov


# ===== DECISÕES (RF-13) =====

@router.post("/decisoes", status_code=status.HTTP_201_CREATED, response_model=DecisaoPropostaResponse)
async def criar_decisao_proposta(
    decisao_data: DecisaoPropostaCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """RF-13: Avaliação e decisão final do governo"""
    decisao = DecisaoProposta(
        **decisao_data.dict(),
        decidida_por_user_id=current_user.id
    )
    db.add(decisao)

    # Atualiza status da proposta
    proposta = db.query(Proposta).filter(Proposta.id == decisao_data.proposta_id).first()
    if proposta:
        if decisao_data.decisao == 'selected':
            proposta.status = 'selected'
        elif decisao_data.decisao == 'rejected':
            proposta.status = 'rejected'

    db.commit()
    db.refresh(decisao)

    return decisao


# ===== DASHBOARD (RF-12) =====

@router.get("/dashboard/{organizacao_id}", response_model=DashboardGovernoResponse)
async def obter_dashboard_governo(
    organizacao_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """RF-12: Dashboard do governo (visão operacional)"""

    # Estatísticas
    demandas_abertas = db.query(Demanda).filter(
        Demanda.organizacao_id == organizacao_id,
        Demanda.status.in_(['draft', 'published'])
    ).count()

    demandas_publicadas = db.query(Demanda).filter(
        Demanda.organizacao_id == organizacao_id,
        Demanda.status == 'published'
    ).count()

    propostas_recebidas = db.query(Proposta).filter(
        Proposta.organizacao_id == organizacao_id
    ).count()

    propostas_pendentes = db.query(Proposta).filter(
        Proposta.organizacao_id == organizacao_id,
        Proposta.status.in_(['pending_validation', 'validated', 'submitted'])
    ).count()

    contratos_ativos = db.query(Contrato).filter(
        Contrato.organizacao_id == organizacao_id,
        Contrato.status.in_(['generated', 'signed'])
    ).count()

    stats = DashboardGovernoStats(
        demandas_abertas=demandas_abertas,
        demandas_publicadas=demandas_publicadas,
        propostas_recebidas=propostas_recebidas,
        propostas_pendentes_avaliacao=propostas_pendentes,
        contratos_ativos=contratos_ativos,
        itens_sem_cobertura=0,  # TODO: Calcular
        prazos_criticos=0  # TODO: Calcular
    )

    # Prazos críticos (demandas que encerram em menos de 7 dias)
    data_limite = datetime.utcnow() + timedelta(days=7)
    demandas_criticas = db.query(Demanda).filter(
        Demanda.organizacao_id == organizacao_id,
        Demanda.status == 'published',
        Demanda.encerra_em <= data_limite,
        Demanda.encerra_em >= datetime.utcnow()
    ).all()

    prazos_criticos = []
    for demanda in demandas_criticas:
        dias_restantes = (demanda.encerra_em - datetime.utcnow()).days
        propostas_count = db.query(Proposta).join(VersaoDemanda).filter(
            VersaoDemanda.demanda_id == demanda.id
        ).count()

        prazos_criticos.append(PrazoCritico(
            demanda_id=demanda.id,
            demanda_titulo=demanda.titulo,
            encerra_em=demanda.encerra_em,
            dias_restantes=dias_restantes,
            propostas_recebidas=propostas_count
        ))

    return DashboardGovernoResponse(
        stats=stats,
        itens_sem_cobertura=[],  # TODO: Implementar
        prazos_criticos=prazos_criticos,
        ultimas_propostas=[]  # TODO: Implementar
    )
