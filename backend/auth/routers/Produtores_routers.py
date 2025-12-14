# routers/Produtores_routers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from schemas.Produtor_schema import (
    PerfilProdutorCreate,
    PerfilProdutorUpdate,
    PerfilProdutorResponse,
    ItemProducaoCreate,
    ItemProducaoUpdate,
    ItemProducaoResponse,
    PeriodoCapacidadeCreate,
    PeriodoCapacidadeUpdate,
    PeriodoCapacidadeResponse,
    DashboardProdutorResponse
)
from models.PerfilProdutor_model import PerfilProdutor
from models.Producao_model import ItemProducao, PeriodoCapacidade
from models.Catalogo_model import CatalogoProduto, Unidade
from models.Documento_model import DocumentoProdutor
from models.Proposta_model import Proposta, ConfirmacaoParticipante
from models.Contrato_model import Contrato
from models.Notificacao_model import Notificacao
from models.User_model import User
from security.security import get_current_user, get_db

router = APIRouter(tags=["Produtores"], prefix="/produtores")


@router.post("/perfil", status_code=status.HTTP_201_CREATED, response_model=PerfilProdutorResponse)
async def criar_perfil_produtor(
    perfil_data: PerfilProdutorCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """RF-04: Cadastro e perfil do produtor"""
    perfil = PerfilProdutor(**perfil_data.dict())
    db.add(perfil)
    db.commit()
    db.refresh(perfil)
    return perfil


@router.get("/perfil/{produtor_id}", response_model=PerfilProdutorResponse)
async def obter_perfil_produtor(
    produtor_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtém perfil do produtor"""
    perfil = db.query(PerfilProdutor).filter(PerfilProdutor.id == produtor_id).first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
    return perfil


@router.patch("/perfil/{produtor_id}", response_model=PerfilProdutorResponse)
async def atualizar_perfil_produtor(
    produtor_id: int,
    perfil_update: PerfilProdutorUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza perfil do produtor"""
    perfil = db.query(PerfilProdutor).filter(PerfilProdutor.id == produtor_id).first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")

    for key, value in perfil_update.dict(exclude_unset=True).items():
        setattr(perfil, key, value)

    db.commit()
    db.refresh(perfil)
    return perfil


@router.post("/producao", status_code=status.HTTP_201_CREATED, response_model=ItemProducaoResponse)
async def criar_item_producao(
    item_data: ItemProducaoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """RF-08: Cadastro de produção, capacidade e sazonalidade"""
    item = ItemProducao(**item_data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/producao/{produtor_id}", response_model=List[ItemProducaoResponse])
async def listar_producao_produtor(
    produtor_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista itens de produção do produtor"""
    itens = db.query(ItemProducao).filter(ItemProducao.produtor_id == produtor_id).all()
    return itens


@router.post("/capacidade", status_code=status.HTTP_201_CREATED, response_model=PeriodoCapacidadeResponse)
async def criar_periodo_capacidade(
    periodo_data: PeriodoCapacidadeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Adiciona período de capacidade para item de produção"""
    periodo = PeriodoCapacidade(**periodo_data.dict(), updated_by_user_id=current_user.id)
    db.add(periodo)
    db.commit()
    db.refresh(periodo)
    return periodo


@router.get("/dashboard/{produtor_id}", response_model=DashboardProdutorResponse)
async def obter_dashboard_produtor(
    produtor_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """RF-09: Dashboard do produtor com pendências"""
    perfil = db.query(PerfilProdutor).filter(PerfilProdutor.id == produtor_id).first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")

    # Contadores
    docs_pendentes = db.query(DocumentoProdutor).filter(
        DocumentoProdutor.produtor_id == produtor_id,
        DocumentoProdutor.status == 'pending'
    ).count()

    docs_aprovados = db.query(DocumentoProdutor).filter(
        DocumentoProdutor.produtor_id == produtor_id,
        DocumentoProdutor.status == 'approved'
    ).count()

    produtos_cadastrados = db.query(ItemProducao).filter(
        ItemProducao.produtor_id == produtor_id,
        ItemProducao.ativo == True
    ).count()

    propostas_ativas = db.query(Proposta).filter(
        Proposta.produtor_id == produtor_id,
        Proposta.status.in_(['draft', 'pending_validation', 'validated'])
    ).count()

    propostas_aguardando = db.query(ConfirmacaoParticipante).filter(
        ConfirmacaoParticipante.produtor_id == produtor_id,
        ConfirmacaoParticipante.status == 'invited'
    ).count()

    notificacoes_nao_lidas = db.query(Notificacao).filter(
        Notificacao.user_id == perfil.user_id,
        Notificacao.lida == False
    ).count()

    # Pendências
    pendencias = []
    if docs_pendentes > 0:
        pendencias.append({"tipo": "documentos", "mensagem": f"{docs_pendentes} documentos pendentes", "prioridade": "alta"})
    if propostas_aguardando > 0:
        pendencias.append({"tipo": "propostas", "mensagem": f"{propostas_aguardando} propostas aguardando resposta", "prioridade": "alta"})

    return DashboardProdutorResponse(
        perfil_id=perfil.id,
        perfil_completo=(perfil.status_perfil == 'complete'),
        documentos_pendentes=docs_pendentes,
        documentos_aprovados=docs_aprovados,
        produtos_cadastrados=produtos_cadastrados,
        demandas_disponiveis=0,  # TODO: Implementar busca de demandas disponíveis
        propostas_ativas=propostas_ativas,
        propostas_aguardando_resposta=propostas_aguardando,
        contratos_ativos=0,  # TODO: Implementar busca de contratos ativos
        notificacoes_nao_lidas=notificacoes_nao_lidas,
        pendencias=pendencias
    )
