# routers/Demanda_routers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List
from decimal import Decimal

from schemas.Demanda_schema import (
    DemandaCreate,
    DemandaResponse,
    ItemDemandaResponse,
    ProdutorCapacidadeResponse,
    ProdutorCapacidadeItem
)
from models.Demanda_model import Demanda, VersaoDemanda, ItemDemanda
from models.User_model import User
from models.Producao_model import ItemProducao, PeriodoCapacidade
from models.PerfilProdutor_model import PerfilProdutor
from models.Catalogo_model import CatalogoProduto, Unidade
from security.security import get_current_user, get_db

router = APIRouter(tags=["Demandas"], prefix="/demandas")


@router.post("", status_code=status.HTTP_201_CREATED, response_model=DemandaResponse)
async def criar_demanda(
    demanda_data: DemandaCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cria uma nova demanda relacionando múltiplos produtos e múltiplos produtores.
    
    Permite relacionar N produtos de N produtores na mesma demanda.
    Exemplo: demanda 1, usuário 1 (produtor), produto 1; demanda 1, usuário 2 (produtor), produto 3, quantidade 500.
    
    Requer autenticação via token JWT.
    Cada user_id nos itens deve ser de um usuário do tipo 'produtor'.
    """
    # Valida produtos, unidades e produtores
    produtores_validados = {}
    
    for item in demanda_data.itens:
        # Valida produto
        produto = db.query(CatalogoProduto).filter(
            CatalogoProduto.id == item.produto_id
        ).first()
        if not produto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produto com ID {item.produto_id} não encontrado no catálogo"
            )
        
        # Valida unidade
        unidade = db.query(Unidade).filter(Unidade.id == item.unidade_id).first()
        if not unidade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unidade com ID {item.unidade_id} não encontrada"
            )
        
        # Valida que o user_id é de um produtor (cache para evitar consultas repetidas)
        if item.user_id not in produtores_validados:
            produtor_user = db.query(User).filter(User.id == item.user_id).first()
            
            if not produtor_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Usuário com ID {item.user_id} não encontrado"
                )
            
            if produtor_user.tipo_usuario != "produtor":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"O usuário com ID {item.user_id} deve ser do tipo 'produtor'. Tipo atual: {produtor_user.tipo_usuario}"
                )
            
            produtores_validados[item.user_id] = produtor_user
    
    # Cria a demanda
    local_entrega_json = None
    if demanda_data.local_entrega:
        local_entrega_json = demanda_data.local_entrega.model_dump()
    
    nova_demanda = Demanda(
        organizacao_id=None,  # Não usa organização
        titulo=demanda_data.titulo,
        descricao=demanda_data.descricao,
        quantidade=demanda_data.quantidade,
        status='draft',
        encerra_em=demanda_data.encerra_em,
        local_entrega_json=local_entrega_json,
        criada_por_user_id=current_user.id  # Usa o usuário autenticado que está criando
    )
    
    db.add(nova_demanda)
    db.flush()
    
    # Cria a versão inicial da demanda
    versao = VersaoDemanda(
        demanda_id=nova_demanda.id,
        numero_versao=1,
        tipo_fonte='manual',
        criada_por_user_id=current_user.id
    )
    
    db.add(versao)
    db.flush()
    
    # Cria os itens da demanda (relacionando produto e produtor)
    for item_data in demanda_data.itens:
        item = ItemDemanda(
            versao_demanda_id=versao.id,
            produto_id=item_data.produto_id,
            user_id=item_data.user_id,  # ID do produtor
            unidade_id=item_data.unidade_id,
            quantidade=item_data.quantidade,
            cronograma_entrega_json=item_data.cronograma_entrega_json,
            preco_maximo=item_data.preco_maximo,
            observacoes=item_data.observacoes
        )
        db.add(item)
    
    db.commit()
    db.refresh(nova_demanda)
    db.refresh(versao)
    
    # Busca os itens com informações dos produtos
    itens = db.query(ItemDemanda).filter(
        ItemDemanda.versao_demanda_id == versao.id
    ).all()
    
    itens_response = []
    for item in itens:
        produto = db.query(CatalogoProduto).filter(
            CatalogoProduto.id == item.produto_id
        ).first()
        unidade = db.query(Unidade).filter(Unidade.id == item.unidade_id).first()
        produtor_user = db.query(User).filter(User.id == item.user_id).first()
        
        itens_response.append(ItemDemandaResponse(
            id=item.id,
            produto_id=item.produto_id,
            user_id=item.user_id,
            user_nome=produtor_user.name if produtor_user else None,
            unidade_id=item.unidade_id,
            quantidade=item.quantidade,
            cronograma_entrega_json=item.cronograma_entrega_json,
            preco_maximo=item.preco_maximo,
            observacoes=item.observacoes,
            produto_nome=produto.nome if produto else None,
            unidade_nome=unidade.nome if unidade else None
        ))
    
    return DemandaResponse(
        id=nova_demanda.id,
        organizacao_id=nova_demanda.organizacao_id,
        titulo=nova_demanda.titulo,
        descricao=nova_demanda.descricao,
        quantidade=nova_demanda.quantidade,
        status=nova_demanda.status,
        publicada_em=nova_demanda.publicada_em,
        encerra_em=nova_demanda.encerra_em,
        local_entrega_json=nova_demanda.local_entrega_json,
        criada_por_user_id=nova_demanda.criada_por_user_id,
        created_at=nova_demanda.created_at,
        updated_at=nova_demanda.updated_at,
        versao_atual=versao.numero_versao,
        itens=itens_response
    )


@router.get("/{demanda_id}", response_model=DemandaResponse)
async def obter_demanda(
    demanda_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtém os detalhes de uma demanda específica, incluindo seus itens.
    """
    demanda = db.query(Demanda).filter(Demanda.id == demanda_id).first()
    
    if not demanda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Demanda não encontrada"
        )
    
    # Busca a versão atual (mais recente)
    versao = db.query(VersaoDemanda).filter(
        VersaoDemanda.demanda_id == demanda_id
    ).order_by(VersaoDemanda.numero_versao.desc()).first()
    
    itens_response = []
    if versao:
        itens = db.query(ItemDemanda).filter(
            ItemDemanda.versao_demanda_id == versao.id
        ).all()
        
        for item in itens:
            produto = db.query(CatalogoProduto).filter(
                CatalogoProduto.id == item.produto_id
            ).first()
            unidade = db.query(Unidade).filter(Unidade.id == item.unidade_id).first()
            produtor_user = db.query(User).filter(User.id == item.user_id).first()
            
            itens_response.append(ItemDemandaResponse(
                id=item.id,
                produto_id=item.produto_id,
                user_id=item.user_id,
                user_nome=produtor_user.name if produtor_user else None,
                unidade_id=item.unidade_id,
                quantidade=item.quantidade,
                cronograma_entrega_json=item.cronograma_entrega_json,
                preco_maximo=item.preco_maximo,
                observacoes=item.observacoes,
                produto_nome=produto.nome if produto else None,
                unidade_nome=unidade.nome if unidade else None
            ))
    
    return DemandaResponse(
        id=demanda.id,
        organizacao_id=demanda.organizacao_id,
        titulo=demanda.titulo,
        descricao=demanda.descricao,
        quantidade=demanda.quantidade,
        status=demanda.status,
        publicada_em=demanda.publicada_em,
        encerra_em=demanda.encerra_em,
        local_entrega_json=demanda.local_entrega_json,
        criada_por_user_id=demanda.criada_por_user_id,
        created_at=demanda.created_at,
        updated_at=demanda.updated_at,
        versao_atual=versao.numero_versao if versao else None,
        itens=itens_response
    )


@router.get("", response_model=List[DemandaResponse])
async def listar_demandas(
    user_id: int = None,
    status: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista todas as demandas, com filtros opcionais por usuário entidade e status.
    """
    query = db.query(Demanda)
    
    if user_id:
        query = query.filter(Demanda.criada_por_user_id == user_id)
    
    if status:
        query = query.filter(Demanda.status == status)
    
    demandas = query.order_by(Demanda.created_at.desc()).all()
    
    result = []
    for demanda in demandas:
        versao = db.query(VersaoDemanda).filter(
            VersaoDemanda.demanda_id == demanda.id
        ).order_by(VersaoDemanda.numero_versao.desc()).first()
        
        itens_response = []
        if versao:
            itens = db.query(ItemDemanda).filter(
                ItemDemanda.versao_demanda_id == versao.id
            ).all()
            
            for item in itens:
                produto = db.query(CatalogoProduto).filter(
                    CatalogoProduto.id == item.produto_id
                ).first()
                unidade = db.query(Unidade).filter(Unidade.id == item.unidade_id).first()
                produtor_user = db.query(User).filter(User.id == item.user_id).first()
                
                itens_response.append(ItemDemandaResponse(
                    id=item.id,
                    produto_id=item.produto_id,
                    user_id=item.user_id,
                    user_nome=produtor_user.name if produtor_user else None,
                    unidade_id=item.unidade_id,
                    quantidade=item.quantidade,
                    cronograma_entrega_json=item.cronograma_entrega_json,
                    preco_maximo=item.preco_maximo,
                    observacoes=item.observacoes,
                    produto_nome=produto.nome if produto else None,
                    unidade_nome=unidade.nome if unidade else None
                ))
        
        result.append(DemandaResponse(
            id=demanda.id,
            organizacao_id=demanda.organizacao_id,
            titulo=demanda.titulo,
            descricao=demanda.descricao,
            quantidade=demanda.quantidade,
            status=demanda.status,
            publicada_em=demanda.publicada_em,
            encerra_em=demanda.encerra_em,
            local_entrega_json=demanda.local_entrega_json,
            criada_por_user_id=demanda.criada_por_user_id,
            created_at=demanda.created_at,
            updated_at=demanda.updated_at,
            versao_atual=versao.numero_versao if versao else None,
            itens=itens_response
        ))
    
    return result


@router.get("/{demanda_id}/produtores", response_model=List[ProdutorCapacidadeResponse])
async def listar_produtores_capacidade(
    demanda_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista todos os produtores que podem suprir (total ou parcialmente) uma demanda.
    Retorna informações sobre quais produtos cada produtor pode fornecer.
    
    Uma demanda pode ser suprida com N produtos de N produtores.
    """
    # Busca a demanda e seus itens
    demanda = db.query(Demanda).filter(Demanda.id == demanda_id).first()
    
    if not demanda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Demanda não encontrada"
        )
    
    # Busca a versão atual
    versao = db.query(VersaoDemanda).filter(
        VersaoDemanda.demanda_id == demanda_id
    ).order_by(VersaoDemanda.numero_versao.desc()).first()
    
    if not versao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Versão da demanda não encontrada"
        )
    
    # Busca os itens da demanda
    itens_demanda = db.query(ItemDemanda).filter(
        ItemDemanda.versao_demanda_id == versao.id
    ).all()
    
    if not itens_demanda:
        return []
    
    # Extrai os IDs dos produtos da demanda
    produtos_demanda_ids = [item.produto_id for item in itens_demanda]
    total_itens_demanda = len(produtos_demanda_ids)
    
    # Busca todos os produtores que têm pelo menos um dos produtos da demanda
    produtores_com_produtos = db.query(PerfilProdutor).join(
        ItemProducao, ItemProducao.produtor_id == PerfilProdutor.id
    ).filter(
        and_(
            ItemProducao.produto_id.in_(produtos_demanda_ids),
            ItemProducao.ativo == True
        )
    ).distinct().all()
    
    resultado = []
    
    for produtor in produtores_com_produtos:
        # Busca os itens de produção do produtor que estão na demanda
        itens_producao = db.query(ItemProducao).filter(
            and_(
                ItemProducao.produtor_id == produtor.id,
                ItemProducao.produto_id.in_(produtos_demanda_ids),
                ItemProducao.ativo == True
            )
        ).all()
        
        itens_disponiveis = []
        produtos_supriveis = set()
        
        for item_prod in itens_producao:
            # Busca o item da demanda correspondente
            item_demanda = next(
                (item for item in itens_demanda if item.produto_id == item_prod.produto_id),
                None
            )
            
            if item_demanda:
                produto = db.query(CatalogoProduto).filter(
                    CatalogoProduto.id == item_prod.produto_id
                ).first()
                unidade = db.query(Unidade).filter(
                    Unidade.id == item_prod.unidade_id
                ).first()
                
                # Busca capacidade do período (se houver)
                periodo = db.query(PeriodoCapacidade).filter(
                    PeriodoCapacidade.item_producao_id == item_prod.id
                ).order_by(PeriodoCapacidade.created_at.desc()).first()
                
                capacidade_periodo = None
                if periodo:
                    capacidade_periodo = {
                        "tipo_periodo": periodo.tipo_periodo,
                        "periodo_inicio": periodo.periodo_inicio.isoformat() if periodo.periodo_inicio else None,
                        "periodo_fim": periodo.periodo_fim.isoformat() if periodo.periodo_fim else None,
                        "quantidade_capacidade": float(periodo.quantidade_capacidade) if periodo.quantidade_capacidade else None,
                        "quantidade_previsao": float(periodo.quantidade_previsao) if periodo.quantidade_previsao else None
                    }
                
                itens_disponiveis.append(ProdutorCapacidadeItem(
                    produto_id=item_prod.produto_id,
                    produto_nome=produto.nome if produto else "Produto desconhecido",
                    unidade_id=item_prod.unidade_id,
                    unidade_nome=unidade.nome if unidade else "Unidade desconhecida",
                    quantidade_disponivel=Decimal(str(periodo.quantidade_capacidade)) if periodo and periodo.quantidade_capacidade else None,
                    preco_base=item_prod.preco_base,
                    capacidade_periodo=capacidade_periodo
                ))
                
                produtos_supriveis.add(item_prod.produto_id)
        
        # Calcula percentual de cobertura
        itens_supriveis = len(produtos_supriveis)
        percentual_cobertura = (itens_supriveis / total_itens_demanda * 100) if total_itens_demanda > 0 else 0
        
        # Busca informações do usuário
        user = db.query(User).filter(User.id == produtor.user_id).first()
        
        resultado.append(ProdutorCapacidadeResponse(
            produtor_id=produtor.id,
            user_id=produtor.user_id,
            nome_produtor=user.name if user else "Produtor desconhecido",
            email=user.email if user else "",
            tipo_produtor=produtor.tipo_produtor,
            itens_disponiveis=itens_disponiveis,
            percentual_cobertura=round(percentual_cobertura, 2),
            total_itens_demanda=total_itens_demanda,
            itens_supriveis=itens_supriveis
        ))
    
    # Ordena por percentual de cobertura (maior primeiro)
    resultado.sort(key=lambda x: x.percentual_cobertura, reverse=True)
    
    return resultado

