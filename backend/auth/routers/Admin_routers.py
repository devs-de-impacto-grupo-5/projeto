# routers/Admin_routers.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta
import csv
import io

from schemas.Admin_schema import (
    SubstituicaoEquivalenciaCreate,
    SubstituicaoEquivalenciaUpdate,
    SubstituicaoEquivalenciaResponse,
    UsuarioAdminResponse,
    UsuarioAdminUpdate,
    EventoAuditoriaResponse,
    RelatorioSistemaResponse,
    DashboardEditalResponse
)
from models.Catalogo_model import SubstitucaoEquivalencia, CatalogoProduto
from models.User_model import User
from models.Organizacao_model import Organizacao
from models.Demanda_model import Demanda, VersaoDemanda
from models.Proposta_model import Proposta
from models.Contrato_model import Contrato
from models.Auditoria_model import EventoAuditoria
from models.PerfilProdutor_model import PerfilProdutor
from security.security import get_current_user, get_db

router = APIRouter(tags=["Admin"], prefix="/admin")


# ===== GESTÃO DE USUÁRIOS (RF-27) =====

@router.get("/usuarios", response_model=List[UsuarioAdminResponse])
async def listar_usuarios(
    tipo_usuario: str = None,
    status: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """RF-27: Gestão de usuários e organizações"""
    query = db.query(User)

    if tipo_usuario:
        query = query.filter(User.tipo_usuario == tipo_usuario)
    if status:
        query = query.filter(User.status == status)

    usuarios = query.all()

    return [UsuarioAdminResponse(
        id=u.id,
        user_id=u.id,
        nome=u.name,
        email=u.email,
        tipo_usuario=u.tipo_usuario,
        subtipo_usuario=u.subtipo_usuario,
        status=u.status,
        role=u.role,
        created_at=u.created_at,
        last_login_at=u.last_login_at
    ) for u in usuarios]


@router.patch("/usuarios/{user_id}", response_model=UsuarioAdminResponse)
async def atualizar_usuario(
    user_id: int,
    usuario_update: UsuarioAdminUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza status ou role de um usuário"""
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    for key, value in usuario_update.dict(exclude_unset=True).items():
        setattr(usuario, key, value)

    db.commit()
    db.refresh(usuario)

    return UsuarioAdminResponse(
        id=usuario.id,
        user_id=usuario.id,
        nome=usuario.name,
        email=usuario.email,
        tipo_usuario=usuario.tipo_usuario,
        subtipo_usuario=usuario.subtipo_usuario,
        status=usuario.status,
        role=usuario.role,
        created_at=usuario.created_at,
        last_login_at=usuario.last_login_at
    )


# ===== GESTÃO DE EQUIVALÊNCIAS (RF-29) =====

@router.post("/equivalencias", status_code=status.HTTP_201_CREATED, response_model=SubstituicaoEquivalenciaResponse)
async def criar_equivalencia(
    equivalencia_data: SubstituicaoEquivalenciaCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """RF-29: Gestão do catálogo e equivalências (substituições)"""
    equivalencia = SubstitucaoEquivalencia(
        **equivalencia_data.dict(),
        aprovado_por_user_id=current_user.id
    )
    db.add(equivalencia)
    db.commit()
    db.refresh(equivalencia)

    return _build_equivalencia_response(equivalencia, db)


@router.get("/equivalencias", response_model=List[SubstituicaoEquivalenciaResponse])
async def listar_equivalencias(
    ativo: bool = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista equivalências de substituição"""
    query = db.query(SubstitucaoEquivalencia)

    if ativo is not None:
        query = query.filter(SubstitucaoEquivalencia.ativo == ativo)

    equivalencias = query.all()
    return [_build_equivalencia_response(e, db) for e in equivalencias]


@router.patch("/equivalencias/{equivalencia_id}", response_model=SubstituicaoEquivalenciaResponse)
async def atualizar_equivalencia(
    equivalencia_id: int,
    equivalencia_update: SubstituicaoEquivalenciaUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza equivalência"""
    equivalencia = db.query(SubstitucaoEquivalencia).filter(
        SubstitucaoEquivalencia.id == equivalencia_id
    ).first()

    if not equivalencia:
        raise HTTPException(status_code=404, detail="Equivalência não encontrada")

    for key, value in equivalencia_update.dict(exclude_unset=True).items():
        setattr(equivalencia, key, value)

    db.commit()
    db.refresh(equivalencia)

    return _build_equivalencia_response(equivalencia, db)


# ===== AUDITORIA =====

@router.get("/auditoria", response_model=List[EventoAuditoriaResponse])
async def listar_eventos_auditoria(
    user_id: int = None,
    entidade_tipo: str = None,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista eventos de auditoria"""
    query = db.query(EventoAuditoria)

    if user_id:
        query = query.filter(EventoAuditoria.user_id == user_id)
    if entidade_tipo:
        query = query.filter(EventoAuditoria.entidade_tipo == entidade_tipo)

    eventos = query.order_by(EventoAuditoria.created_at.desc()).limit(limit).all()

    return [EventoAuditoriaResponse(
        id=e.id,
        user_id=e.user_id,
        user_nome=e.user.name if e.user else None,
        acao=e.acao,
        entidade_tipo=e.entidade_tipo,
        entidade_id=e.entidade_id,
        detalhes=e.detalhes,
        ip_address=e.ip_address,
        created_at=e.created_at
    ) for e in eventos]


# ===== RELATÓRIOS =====

@router.get("/relatorio", response_model=RelatorioSistemaResponse)
async def obter_relatorio_sistema(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Relatório geral do sistema"""
    total_usuarios = db.query(User).count()
    total_produtores = db.query(User).filter(User.tipo_usuario == 'produtor').count()
    total_governo = db.query(User).filter(User.tipo_usuario == 'entidade_executora').count()
    total_organizacoes = db.query(Organizacao).count()
    total_demandas = db.query(Demanda).count()
    total_propostas = db.query(Proposta).count()
    total_contratos = db.query(Contrato).count()
    total_produtos_catalogo = db.query(CatalogoProduto).filter(CatalogoProduto.ativo == True).count()

    # Últimos 30 dias
    data_limite = datetime.utcnow() - timedelta(days=30)

    usuarios_ativos = db.query(User).filter(User.last_login_at >= data_limite).count()
    demandas_publicadas = db.query(Demanda).filter(
        Demanda.publicada_em >= data_limite
    ).count()
    propostas_criadas = db.query(Proposta).filter(
        Proposta.created_at >= data_limite
    ).count()
    contratos_assinados = db.query(Contrato).filter(
        Contrato.assinado_em >= data_limite
    ).count()

    return RelatorioSistemaResponse(
        total_usuarios=total_usuarios,
        total_produtores=total_produtores,
        total_governo=total_governo,
        total_organizacoes=total_organizacoes,
        total_demandas=total_demandas,
        total_propostas=total_propostas,
        total_contratos=total_contratos,
        total_produtos_catalogo=total_produtos_catalogo,
        usuarios_ativos_ultimos_30_dias=usuarios_ativos,
        demandas_publicadas_ultimos_30_dias=demandas_publicadas,
        propostas_criadas_ultimos_30_dias=propostas_criadas,
        contratos_assinados_ultimos_30_dias=contratos_assinados
    )


@router.get("/relatorio/download")
async def baixar_relatorio_editais(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Gera e baixa um relatório CSV dos editais"""
    demandas = db.query(Demanda).order_by(Demanda.created_at.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Cabeçalho do CSV
    writer.writerow(['ID', 'Título', 'Status', 'Data Criação', 'Quantidade Total', 'Candidatos'])
    
    for demanda in demandas:
        # Busca contagem de candidatos
        versao = db.query(VersaoDemanda).filter(
            VersaoDemanda.demanda_id == demanda.id
        ).order_by(VersaoDemanda.numero_versao.desc()).first()
        
        candidatos_count = 0
        if versao:
            candidatos_count = db.query(Proposta).filter(
                Proposta.versao_demanda_id == versao.id
            ).count()
            
        writer.writerow([
            demanda.id,
            demanda.titulo,
            demanda.status,
            demanda.created_at.strftime("%d/%m/%Y"),
            demanda.quantidade or 0,
            candidatos_count
        ])
    
    output.seek(0)
    
    response = StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = "attachment; filename=relatorio_editais.csv"
    return response


@router.get("/editais/{demanda_id}/download")
async def baixar_detalhes_edital(
    demanda_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Gera CSV com detalhes do edital e candidatos"""
    demanda = db.query(Demanda).filter(Demanda.id == demanda_id).first()
    if not demanda:
        raise HTTPException(status_code=404, detail="Edital não encontrado")

    output = io.StringIO()
    writer = csv.writer(output)
    
    # Cabeçalho do Edital
    writer.writerow(["Detalhes do Edital"])
    writer.writerow(["ID", "Título", "Status", "Data Criação", "Descrição"])
    writer.writerow([
        demanda.id,
        demanda.titulo,
        demanda.status,
        demanda.created_at.strftime("%d/%m/%Y"),
        demanda.descricao
    ])
    writer.writerow([])
    
    # Candidatos
    writer.writerow(["Candidatos"])
    writer.writerow(["ID Proposta", "Produtor", "Status", "Valor", "Data Proposta"])
    
    versao = db.query(VersaoDemanda).filter(
        VersaoDemanda.demanda_id == demanda.id
    ).order_by(VersaoDemanda.numero_versao.desc()).first()
    
    if versao:
        propostas = db.query(Proposta).filter(
            Proposta.versao_demanda_id == versao.id
        ).all()
        
        for proposta in propostas:
            produtor = db.query(User).filter(User.id == proposta.produtor_id).first()
            writer.writerow([
                proposta.id,
                produtor.name if produtor else "Desconhecido",
                proposta.status,
                proposta.valor_total,
                proposta.created_at.strftime("%d/%m/%Y")
            ])
            
    output.seek(0)
    
    response = StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = f"attachment; filename=edital_{demanda_id}_detalhes.csv"
    return response


@router.get("/dashboard/editais", response_model=List[DashboardEditalResponse])
async def listar_editais_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista editais para o dashboard com contagem de candidatos"""
    demandas = db.query(Demanda).order_by(Demanda.created_at.desc()).limit(50).all()
    
    result = []
    for demanda in demandas:
        # Busca a versão mais recente
        versao = db.query(VersaoDemanda).filter(
            VersaoDemanda.demanda_id == demanda.id
        ).order_by(VersaoDemanda.numero_versao.desc()).first()
        
        candidatos_count = 0
        if versao:
            candidatos_count = db.query(Proposta).filter(
                Proposta.versao_demanda_id == versao.id
            ).count()
            
        result.append(DashboardEditalResponse(
            id=demanda.id,
            titulo=demanda.titulo,
            candidatos=candidatos_count,
            data=demanda.created_at,
            status=demanda.status
        ))
        
    return result


# ===== FUNÇÕES AUXILIARES =====

def _build_equivalencia_response(equivalencia: SubstitucaoEquivalencia, db: Session) -> SubstituicaoEquivalenciaResponse:
    """Constrói resposta de equivalência com nomes dos produtos"""
    produto_origem = db.query(CatalogoProduto).filter(
        CatalogoProduto.id == equivalencia.from_product_id
    ).first()
    produto_destino = db.query(CatalogoProduto).filter(
        CatalogoProduto.id == equivalencia.to_product_id
    ).first()
    usuario = db.query(User).filter(User.id == equivalencia.aprovado_por_user_id).first()

    return SubstituicaoEquivalenciaResponse(
        id=equivalencia.id,
        from_product_id=equivalencia.from_product_id,
        to_product_id=equivalencia.to_product_id,
        razao_equivalencia=equivalencia.razao_equivalencia,
        observacoes=equivalencia.observacoes,
        ativo=equivalencia.ativo,
        aprovado_por_user_id=equivalencia.aprovado_por_user_id,
        aprovado_por_nome=usuario.name if usuario else None,
        produto_origem_nome=produto_origem.nome if produto_origem else None,
        produto_destino_nome=produto_destino.nome if produto_destino else None,
        created_at=equivalencia.created_at
    )
