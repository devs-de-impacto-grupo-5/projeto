# routers/Contratos_routers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from schemas.Contrato_schema import (
    ContratoCreate,
    ContratoUpdate,
    ContratoResponse,
    RegistroBlockchainCreate,
    RegistroBlockchainUpdate,
    RegistroBlockchainResponse
)
from models.Contrato_model import Contrato, ModeloContrato
from models.Blockchain_model import RegistroBlockchain
from models.Proposta_model import Proposta
from models.Demanda_model import Demanda
from models.Organizacao_model import Organizacao
from models.User_model import User
from security.security import get_current_user, get_db
import hashlib
from datetime import datetime

router = APIRouter(tags=["Contratos"], prefix="/contratos")


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ContratoResponse)
async def criar_contrato(
    contrato_data: ContratoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """RF-23: Geração de contrato a partir da proposta vencedora"""
    # Valida proposta
    proposta = db.query(Proposta).filter(Proposta.id == contrato_data.proposta_id).first()
    if not proposta:
        raise HTTPException(status_code=404, detail="Proposta não encontrada")

    if proposta.status != 'selected':
        raise HTTPException(status_code=400, detail="Apenas propostas selecionadas podem gerar contrato")

    # Cria contrato
    contrato = Contrato(**contrato_data.dict(), status='draft')
    db.add(contrato)
    db.commit()
    db.refresh(contrato)

    return _build_contrato_response(contrato, db)


@router.get("/{contrato_id}", response_model=ContratoResponse)
async def obter_contrato(
    contrato_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtém detalhes de um contrato"""
    contrato = db.query(Contrato).filter(Contrato.id == contrato_id).first()
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato não encontrado")

    return _build_contrato_response(contrato, db)


@router.get("", response_model=List[ContratoResponse])
async def listar_contratos(
    organizacao_id: Optional[int] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista contratos com filtros opcionais"""
    query = db.query(Contrato)

    if organizacao_id:
        query = query.filter(Contrato.organizacao_id == organizacao_id)
    if status:
        query = query.filter(Contrato.status == status)

    contratos = query.order_by(Contrato.gerado_em.desc()).all()
    return [_build_contrato_response(c, db) for c in contratos]


@router.patch("/{contrato_id}", response_model=ContratoResponse)
async def atualizar_contrato(
    contrato_id: int,
    contrato_update: ContratoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza status do contrato"""
    contrato = db.query(Contrato).filter(Contrato.id == contrato_id).first()
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato não encontrado")

    if contrato_update.status:
        contrato.status = contrato_update.status
        if contrato_update.status == 'generated':
            contrato.gerado_em = datetime.utcnow()
        elif contrato_update.status == 'signed':
            contrato.assinado_em = datetime.utcnow()

    if contrato_update.arquivo_contrato_id:
        contrato.arquivo_contrato_id = contrato_update.arquivo_contrato_id

    db.commit()
    db.refresh(contrato)

    return _build_contrato_response(contrato, db)


# ===== BLOCKCHAIN (RF-24) =====

@router.post("/{contrato_id}/blockchain", status_code=status.HTTP_201_CREATED, response_model=RegistroBlockchainResponse)
async def registrar_contrato_blockchain(
    contrato_id: int,
    registro_data: RegistroBlockchainCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """RF-24: Registro em blockchain (prova de integridade)"""
    contrato = db.query(Contrato).filter(Contrato.id == contrato_id).first()
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato não encontrado")

    # Verifica se já existe registro
    registro_existente = db.query(RegistroBlockchain).filter(
        RegistroBlockchain.contrato_id == contrato_id
    ).first()

    if registro_existente:
        raise HTTPException(status_code=400, detail="Contrato já possui registro em blockchain")

    # Cria registro
    registro = RegistroBlockchain(**registro_data.dict(), status='pending')
    db.add(registro)
    db.commit()
    db.refresh(registro)

    # TODO: Integrar com serviço de blockchain real
    # Por enquanto, apenas simula

    return registro


@router.patch("/blockchain/{registro_id}", response_model=RegistroBlockchainResponse)
async def atualizar_registro_blockchain(
    registro_id: int,
    registro_update: RegistroBlockchainUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza registro de blockchain com hash da transação"""
    registro = db.query(RegistroBlockchain).filter(RegistroBlockchain.id == registro_id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro não encontrado")

    for key, value in registro_update.dict(exclude_unset=True).items():
        setattr(registro, key, value)

    if registro_update.status == 'confirmed':
        registro.verificado_em = datetime.utcnow()

    db.commit()
    db.refresh(registro)

    return registro


@router.get("/{contrato_id}/blockchain", response_model=RegistroBlockchainResponse)
async def obter_registro_blockchain(
    contrato_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtém registro de blockchain do contrato"""
    registro = db.query(RegistroBlockchain).filter(
        RegistroBlockchain.contrato_id == contrato_id
    ).first()

    if not registro:
        raise HTTPException(status_code=404, detail="Registro de blockchain não encontrado")

    return registro


# ===== FUNÇÕES AUXILIARES =====

def _build_contrato_response(contrato: Contrato, db: Session) -> ContratoResponse:
    """Constrói resposta de contrato com informações adicionais"""
    org = db.query(Organizacao).filter(Organizacao.id == contrato.organizacao_id).first()
    demanda = db.query(Demanda).filter(Demanda.id == contrato.demanda_id).first()

    # Verifica se tem registro blockchain
    registro_blockchain = db.query(RegistroBlockchain).filter(
        RegistroBlockchain.contrato_id == contrato.id
    ).first()

    return ContratoResponse(
        id=contrato.id,
        organizacao_id=contrato.organizacao_id,
        demanda_id=contrato.demanda_id,
        proposta_id=contrato.proposta_id,
        modelo_id=contrato.modelo_id,
        status=contrato.status,
        arquivo_contrato_id=contrato.arquivo_contrato_id,
        gerado_em=contrato.gerado_em,
        assinado_em=contrato.assinado_em,
        organizacao_nome=org.nome if org else None,
        demanda_titulo=demanda.titulo if demanda else None,
        blockchain_registrado=registro_blockchain is not None,
        blockchain_transaction_hash=registro_blockchain.transaction_hash if registro_blockchain else None
    )
