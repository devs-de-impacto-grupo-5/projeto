# routers/Propostas_routers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime, timedelta

from schemas.Proposta_schema import (
    PropostaCreate,
    PropostaResponse,
    PropostaUpdate,
    ItemPropostaResponse,
    ConfirmacaoParticipanteCreate,
    ConfirmacaoParticipanteUpdate,
    ConfirmacaoParticipanteResponse,
    SubmissaoPropostaCreate,
    SubmissaoPropostaUpdate,
    SubmissaoPropostaResponse,
    EtapaSubmissaoFisicaUpdate,
    EtapaSubmissaoFisicaResponse
)
from models.Proposta_model import (
    Proposta,
    ItemProposta,
    ConfirmacaoParticipante,
    ReservaCapacidade
)
from models.Submissao_model import SubmissaoProposta, EtapaSubmissaoFisica
from models.Demanda_model import VersaoDemanda, ItemDemanda
from models.PerfilProdutor_model import PerfilProdutor
from models.Catalogo_model import CatalogoProduto, Unidade
from models.User_model import User
from security.security import get_current_user, get_db

router = APIRouter(tags=["Propostas"], prefix="/propostas")


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PropostaResponse)
async def criar_proposta(
    proposta_data: PropostaCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cria uma nova proposta para uma demanda.
    RF-17: Geração automática de proposta
    """
    # Valida versão da demanda
    versao = db.query(VersaoDemanda).filter(VersaoDemanda.id == proposta_data.versao_demanda_id).first()
    if not versao:
        raise HTTPException(status_code=404, detail="Versão da demanda não encontrada")

    # Valida tipo de proposta
    if proposta_data.tipo_proposta == "single" and not proposta_data.produtor_id:
        raise HTTPException(status_code=400, detail="Proposta individual requer produtor_id")
    if proposta_data.tipo_proposta == "group" and not proposta_data.grupo_id:
        raise HTTPException(status_code=400, detail="Proposta de grupo requer grupo_id")

    # Cria proposta
    nova_proposta = Proposta(
        versao_demanda_id=proposta_data.versao_demanda_id,
        organizacao_id=proposta_data.organizacao_id,
        tipo_proposta=proposta_data.tipo_proposta,
        produtor_id=proposta_data.produtor_id,
        grupo_id=proposta_data.grupo_id,
        valor_total=proposta_data.valor_total,
        status='draft',
        criada_por_user_id=current_user.id
    )

    db.add(nova_proposta)
    db.flush()

    # Cria itens da proposta
    for item_data in proposta_data.itens:
        item = ItemProposta(
            proposta_id=nova_proposta.id,
            item_demanda_id=item_data.item_demanda_id,
            produto_id=item_data.produto_id,
            unidade_id=item_data.unidade_id,
            quantidade=item_data.quantidade,
            preco=item_data.preco,
            substituto_de_produto_id=item_data.substituto_de_produto_id,
            motivo_substituicao=item_data.motivo_substituicao,
            flag_aviso=item_data.flag_aviso
        )
        db.add(item)

    db.commit()
    db.refresh(nova_proposta)

    return _build_proposta_response(nova_proposta, db)


@router.get("/{proposta_id}", response_model=PropostaResponse)
async def obter_proposta(
    proposta_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtém detalhes de uma proposta específica"""
    proposta = db.query(Proposta).filter(Proposta.id == proposta_id).first()
    if not proposta:
        raise HTTPException(status_code=404, detail="Proposta não encontrada")

    return _build_proposta_response(proposta, db)


@router.get("", response_model=List[PropostaResponse])
async def listar_propostas(
    versao_demanda_id: Optional[int] = None,
    organizacao_id: Optional[int] = None,
    produtor_id: Optional[int] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista propostas com filtros opcionais"""
    query = db.query(Proposta)

    if versao_demanda_id:
        query = query.filter(Proposta.versao_demanda_id == versao_demanda_id)
    if organizacao_id:
        query = query.filter(Proposta.organizacao_id == organizacao_id)
    if produtor_id:
        query = query.filter(Proposta.produtor_id == produtor_id)
    if status:
        query = query.filter(Proposta.status == status)

    propostas = query.order_by(Proposta.created_at.desc()).all()

    return [_build_proposta_response(p, db) for p in propostas]


@router.patch("/{proposta_id}", response_model=PropostaResponse)
async def atualizar_proposta(
    proposta_id: int,
    proposta_update: PropostaUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza status ou valor de uma proposta"""
    proposta = db.query(Proposta).filter(Proposta.id == proposta_id).first()
    if not proposta:
        raise HTTPException(status_code=404, detail="Proposta não encontrada")

    if proposta_update.status:
        proposta.status = proposta_update.status
    if proposta_update.valor_total is not None:
        proposta.valor_total = proposta_update.valor_total

    db.commit()
    db.refresh(proposta)

    return _build_proposta_response(proposta, db)


# ===== CONFIRMAÇÕES DE PARTICIPANTES (RF-18) =====

@router.post("/{proposta_id}/confirmacoes", status_code=status.HTTP_201_CREATED, response_model=ConfirmacaoParticipanteResponse)
async def criar_confirmacao_participante(
    proposta_id: int,
    confirmacao_data: ConfirmacaoParticipanteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Convida um produtor para participar de uma proposta.
    RF-18: Validação com produtores (aceitar/recusar participação)
    """
    proposta = db.query(Proposta).filter(Proposta.id == proposta_id).first()
    if not proposta:
        raise HTTPException(status_code=404, detail="Proposta não encontrada")

    # Verifica se já existe confirmação
    confirmacao_existente = db.query(ConfirmacaoParticipante).filter(
        and_(
            ConfirmacaoParticipante.proposta_id == proposta_id,
            ConfirmacaoParticipante.produtor_id == confirmacao_data.produtor_id
        )
    ).first()

    if confirmacao_existente:
        raise HTTPException(status_code=400, detail="Produtor já foi convidado para esta proposta")

    # Cria confirmação com prazo de expiração
    expira_em = datetime.utcnow() + timedelta(days=7)  # 7 dias para responder

    confirmacao = ConfirmacaoParticipante(
        proposta_id=proposta_id,
        produtor_id=confirmacao_data.produtor_id,
        status='invited',
        expira_em=expira_em
    )

    db.add(confirmacao)
    db.commit()
    db.refresh(confirmacao)

    # TODO: Enviar notificação para o produtor

    return _build_confirmacao_response(confirmacao, db)


@router.patch("/confirmacoes/{confirmacao_id}", response_model=ConfirmacaoParticipanteResponse)
async def responder_confirmacao(
    confirmacao_id: int,
    confirmacao_update: ConfirmacaoParticipanteUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Produtor aceita ou recusa participação em uma proposta.
    RF-18: Validação com produtores
    """
    confirmacao = db.query(ConfirmacaoParticipante).filter(ConfirmacaoParticipante.id == confirmacao_id).first()
    if not confirmacao:
        raise HTTPException(status_code=404, detail="Confirmação não encontrada")

    # Verifica se já expirou
    if confirmacao.expira_em and datetime.utcnow() > confirmacao.expira_em:
        confirmacao.status = 'expired'
        db.commit()
        raise HTTPException(status_code=400, detail="Prazo de resposta expirado")

    # Atualiza status
    confirmacao.status = confirmacao_update.status
    confirmacao.motivo_recusa = confirmacao_update.motivo_recusa
    confirmacao.respondido_em = datetime.utcnow()

    db.commit()
    db.refresh(confirmacao)

    # RF-19: Se recusou, tentar substituição automática
    if confirmacao.status == 'declined':
        # TODO: Implementar lógica de substituição automática
        pass

    # TODO: Enviar notificação para o governo

    return _build_confirmacao_response(confirmacao, db)


@router.get("/{proposta_id}/confirmacoes", response_model=List[ConfirmacaoParticipanteResponse])
async def listar_confirmacoes(
    proposta_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista todas as confirmações de uma proposta"""
    confirmacoes = db.query(ConfirmacaoParticipante).filter(
        ConfirmacaoParticipante.proposta_id == proposta_id
    ).all()

    return [_build_confirmacao_response(c, db) for c in confirmacoes]


# ===== SUBMISSÃO (RF-21, RF-22) =====

@router.post("/{proposta_id}/submissao", status_code=status.HTTP_201_CREATED, response_model=SubmissaoPropostaResponse)
async def criar_submissao(
    proposta_id: int,
    submissao_data: SubmissaoPropostaCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Inicia processo de submissão de proposta (digital ou física).
    RF-21: Submissão digital
    RF-22: Submissão modo físico
    """
    proposta = db.query(Proposta).filter(Proposta.id == proposta_id).first()
    if not proposta:
        raise HTTPException(status_code=404, detail="Proposta não encontrada")

    # Verifica se já existe submissão
    submissao_existente = db.query(SubmissaoProposta).filter(
        SubmissaoProposta.proposta_id == proposta_id
    ).first()

    if submissao_existente:
        raise HTTPException(status_code=400, detail="Proposta já possui submissão")

    # Cria submissão
    submissao = SubmissaoProposta(
        proposta_id=proposta_id,
        tipo_submissao=submissao_data.tipo_submissao,
        status='not_started',
        observacoes=submissao_data.observacoes
    )

    db.add(submissao)
    db.flush()

    # Se for submissão física, cria etapas do checklist
    if submissao_data.tipo_submissao == 'physical':
        etapas_padrao = [
            {"numero": 1, "titulo": "Imprimir proposta", "descricao": "Imprimir documento da proposta"},
            {"numero": 2, "titulo": "Assinar documento", "descricao": "Assinar todas as páginas necessárias"},
            {"numero": 3, "titulo": "Montar envelope", "descricao": "Organizar documentos no envelope"},
            {"numero": 4, "titulo": "Protocolar entrega", "descricao": "Entregar no local indicado e obter protocolo"}
        ]

        for etapa_data in etapas_padrao:
            etapa = EtapaSubmissaoFisica(
                submissao_proposta_id=submissao.id,
                numero_etapa=etapa_data["numero"],
                titulo=etapa_data["titulo"],
                descricao=etapa_data["descricao"],
                status='todo'
            )
            db.add(etapa)

    db.commit()
    db.refresh(submissao)

    return _build_submissao_response(submissao, db)


@router.patch("/submissoes/{submissao_id}", response_model=SubmissaoPropostaResponse)
async def atualizar_submissao(
    submissao_id: int,
    submissao_update: SubmissaoPropostaUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza status da submissão"""
    submissao = db.query(SubmissaoProposta).filter(SubmissaoProposta.id == submissao_id).first()
    if not submissao:
        raise HTTPException(status_code=404, detail="Submissão não encontrada")

    if submissao_update.status:
        submissao.status = submissao_update.status
        if submissao_update.status == 'submitted':
            submissao.submetida_em = datetime.utcnow()

    if submissao_update.observacoes:
        submissao.observacoes = submissao_update.observacoes

    db.commit()
    db.refresh(submissao)

    return _build_submissao_response(submissao, db)


@router.patch("/submissoes/etapas/{etapa_id}", response_model=EtapaSubmissaoFisicaResponse)
async def atualizar_etapa_submissao(
    etapa_id: int,
    etapa_update: EtapaSubmissaoFisicaUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Marca etapa de submissão física como concluída ou pulada"""
    etapa = db.query(EtapaSubmissaoFisica).filter(EtapaSubmissaoFisica.id == etapa_id).first()
    if not etapa:
        raise HTTPException(status_code=404, detail="Etapa não encontrada")

    etapa.status = etapa_update.status
    if etapa_update.status == 'done':
        etapa.concluida_em = datetime.utcnow()

    db.commit()
    db.refresh(etapa)

    return EtapaSubmissaoFisicaResponse.from_orm(etapa)


# ===== FUNÇÕES AUXILIARES =====

def _build_proposta_response(proposta: Proposta, db: Session) -> PropostaResponse:
    """Constrói resposta completa de proposta com itens"""
    itens = db.query(ItemProposta).filter(ItemProposta.proposta_id == proposta.id).all()

    itens_response = []
    for item in itens:
        produto = db.query(CatalogoProduto).filter(CatalogoProduto.id == item.produto_id).first()
        unidade = db.query(Unidade).filter(Unidade.id == item.unidade_id).first()

        itens_response.append(ItemPropostaResponse(
            id=item.id,
            proposta_id=item.proposta_id,
            item_demanda_id=item.item_demanda_id,
            produto_id=item.produto_id,
            unidade_id=item.unidade_id,
            quantidade=item.quantidade,
            preco=item.preco,
            substituto_de_produto_id=item.substituto_de_produto_id,
            motivo_substituicao=item.motivo_substituicao,
            flag_aviso=item.flag_aviso,
            produto_nome=produto.nome if produto else None,
            unidade_nome=unidade.nome if unidade else None,
            created_at=item.created_at
        ))

    return PropostaResponse(
        id=proposta.id,
        versao_demanda_id=proposta.versao_demanda_id,
        organizacao_id=proposta.organizacao_id,
        tipo_proposta=proposta.tipo_proposta,
        produtor_id=proposta.produtor_id,
        grupo_id=proposta.grupo_id,
        status=proposta.status,
        valor_total=proposta.valor_total,
        criada_por_user_id=proposta.criada_por_user_id,
        created_at=proposta.created_at,
        updated_at=proposta.updated_at,
        itens=itens_response
    )


def _build_confirmacao_response(confirmacao: ConfirmacaoParticipante, db: Session) -> ConfirmacaoParticipanteResponse:
    """Constrói resposta de confirmação com nome do produtor"""
    produtor = db.query(PerfilProdutor).filter(PerfilProdutor.id == confirmacao.produtor_id).first()
    produtor_nome = None
    if produtor and produtor.user:
        produtor_nome = produtor.user.name

    return ConfirmacaoParticipanteResponse(
        id=confirmacao.id,
        proposta_id=confirmacao.proposta_id,
        produtor_id=confirmacao.produtor_id,
        status=confirmacao.status,
        motivo_recusa=confirmacao.motivo_recusa,
        convidado_em=confirmacao.convidado_em,
        respondido_em=confirmacao.respondido_em,
        expira_em=confirmacao.expira_em,
        produtor_nome=produtor_nome
    )


def _build_submissao_response(submissao: SubmissaoProposta, db: Session) -> SubmissaoPropostaResponse:
    """Constrói resposta de submissão com etapas"""
    etapas = db.query(EtapaSubmissaoFisica).filter(
        EtapaSubmissaoFisica.submissao_proposta_id == submissao.id
    ).order_by(EtapaSubmissaoFisica.numero_etapa).all()

    etapas_response = [EtapaSubmissaoFisicaResponse.from_orm(e) for e in etapas]

    return SubmissaoPropostaResponse(
        id=submissao.id,
        proposta_id=submissao.proposta_id,
        tipo_submissao=submissao.tipo_submissao,
        status=submissao.status,
        submetida_em=submissao.submetida_em,
        arquivo_comprovante_id=submissao.arquivo_comprovante_id,
        observacoes=submissao.observacoes,
        etapas_fisica=etapas_response
    )
