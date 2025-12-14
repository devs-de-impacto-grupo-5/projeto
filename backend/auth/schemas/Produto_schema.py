from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProdutoCreate(BaseModel):
    """Schema para criar um novo produto"""
    nome: str = Field(..., min_length=1, max_length=255)
    descricao: Optional[str] = Field(None, max_length=1000)
    categoria: str = Field(..., min_length=1, max_length=100)
    preco: float = Field(..., gt=0, description="Preço deve ser maior que 0")


class ProdutoUpdate(BaseModel):
    """Schema para atualizar um produto"""
    nome: Optional[str] = Field(None, min_length=1, max_length=255)
    descricao: Optional[str] = Field(None, max_length=1000)
    categoria: Optional[str] = Field(None, min_length=1, max_length=100)
    preco: Optional[float] = Field(None, gt=0)


class ProdutoResponse(BaseModel):
    """Schema para resposta de produto"""
    id: int
    nome: str
    descricao: Optional[str]
    categoria: str
    preco: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProdutoListResponse(BaseModel):
    """Schema para listar produtos"""
    total: int
    produtos: list[ProdutoResponse]
