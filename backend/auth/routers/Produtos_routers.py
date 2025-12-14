from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.Produto_schema import (
    ProdutoCreate,
    ProdutoUpdate,
    ProdutoResponse,
    ProdutoListResponse
)
from models.Conta_model import Produto
from models.User_model import User
from security.security import get_current_user, get_db

router = APIRouter(tags=["Produtos"], prefix="/produtos")


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ProdutoResponse)
async def criar_produto(
    produto_data: ProdutoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cria um novo produto para o usuário autenticado.
    Requer autenticação via token JWT.
    """
    # Cria o novo produto
    novo_produto = Produto(
        user_id=current_user.id,
        nome=produto_data.nome,
        descricao=produto_data.descricao,
        categoria=produto_data.categoria,
        preco=produto_data.preco
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto


@router.get("", response_model=ProdutoListResponse)
async def listar_produtos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista todos os produtos do usuário autenticado.
    Requer autenticação via token JWT.
    """
    produtos = db.query(Produto).filter(Produto.user_id == current_user.id).all()

    return ProdutoListResponse(
        total=len(produtos),
        produtos=produtos
    )


@router.get("/{produto_id}", response_model=ProdutoResponse)
async def obter_produto(
    produto_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtém detalhes de um produto específico.
    O usuário só pode acessar seus próprios produtos.
    Requer autenticação via token JWT.
    """
    produto = db.query(Produto).filter(
        Produto.id == produto_id,
        Produto.user_id == current_user.id
    ).first()

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )

    return produto


@router.put("/{produto_id}", response_model=ProdutoResponse)
async def atualizar_produto(
    produto_id: int,
    produto_data: ProdutoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza um produto existente.
    O usuário só pode atualizar seus próprios produtos.
    Requer autenticação via token JWT.
    """
    produto = db.query(Produto).filter(
        Produto.id == produto_id,
        Produto.user_id == current_user.id
    ).first()

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )

    # Atualiza apenas os campos fornecidos
    if produto_data.nome is not None:
        produto.nome = produto_data.nome
    if produto_data.descricao is not None:
        produto.descricao = produto_data.descricao
    if produto_data.categoria is not None:
        produto.categoria = produto_data.categoria
    if produto_data.preco is not None:
        produto.preco = produto_data.preco

    db.commit()
    db.refresh(produto)

    return produto


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_produto(
    produto_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deleta um produto.
    O usuário só pode deletar seus próprios produtos.
    Requer autenticação via token JWT.
    """
    produto = db.query(Produto).filter(
        Produto.id == produto_id,
        Produto.user_id == current_user.id
    ).first()

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )

    db.delete(produto)
    db.commit()

    return None
