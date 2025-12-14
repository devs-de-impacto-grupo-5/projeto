# schemas/Demanda_schema.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal


class ItemDemandaCreate(BaseModel):
    """Schema para criar um item de demanda - relaciona produto e produtor"""
    produto_id: int = Field(..., description="ID do produto do catálogo")
    user_id: int = Field(..., description="ID do usuário produtor que irá fornecer este produto")
    unidade_id: int = Field(..., description="ID da unidade de medida")
    quantidade: Decimal = Field(..., gt=0, description="Quantidade necessária")
    cronograma_entrega_json: Optional[Dict[str, Any]] = Field(
        None, 
        description="Cronograma de entrega em formato JSON (parcelas/datas)"
    )
    preco_maximo: Optional[Decimal] = Field(None, description="Preço máximo aceito (opcional)")
    observacoes: Optional[str] = Field(None, description="Observações sobre o item")


class LocalEntrega(BaseModel):
    """Schema para local de entrega"""
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    cep: Optional[str] = None
    coords: Optional[Dict[str, float]] = None  # {latitude, longitude}


class DemandaCreate(BaseModel):
    """Schema para criar uma demanda
    
    Permite relacionar múltiplos produtos e múltiplos produtores na mesma demanda.
    Cada item relaciona um produto com um produtor específico.
    Exemplo: demanda 1, usuário 1 (produtor), produto 1; demanda 1, usuário 2 (produtor), produto 3, quantidade 500.
    """
    titulo: str = Field(..., min_length=1, max_length=500, description="Título da demanda")
    descricao: Optional[str] = Field(None, description="Descrição detalhada da demanda")
    quantidade: Optional[int] = Field(None, gt=0, description="Quantidade total da demanda (opcional)")
    itens: List[ItemDemandaCreate] = Field(..., min_items=1, description="Lista de itens relacionando produtos e produtores")
    encerra_em: Optional[datetime] = Field(None, description="Data/hora de encerramento da demanda")
    local_entrega: Optional[LocalEntrega] = Field(None, description="Local de entrega")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "titulo": "Demanda de Alimentos para Merenda Escolar - Janeiro 2025",
                    "descricao": "Demanda de produtos alimentícios para merenda escolar do mês de janeiro",
                    "quantidade": 1500,
                    "itens": [
                        {
                            "produto_id": 1,
                            "user_id": 1,
                            "unidade_id": 1,
                            "quantidade": "1000.00",
                            "preco_maximo": "5.50",
                            "observacoes": "Arroz tipo 1, preferencialmente orgânico"
                        },
                        {
                            "produto_id": 3,
                            "user_id": 2,
                            "unidade_id": 2,
                            "quantidade": "500.00",
                            "preco_maximo": "8.00",
                            "observacoes": "Feijão preto"
                        }
                    ],
                    "encerra_em": "2025-01-15T23:59:59",
                    "local_entrega": {
                        "endereco": "Rua das Escolas, 123",
                        "cidade": "Rio de Janeiro",
                        "uf": "RJ",
                        "cep": "20000-000"
                    }
                }
            ]
        }
    }


class ItemDemandaResponse(BaseModel):
    """Schema de resposta para item de demanda"""
    id: int
    produto_id: int
    user_id: int = Field(..., description="ID do produtor")
    user_nome: Optional[str] = Field(None, description="Nome do produtor")
    unidade_id: int
    quantidade: Decimal
    cronograma_entrega_json: Optional[Dict[str, Any]] = None
    preco_maximo: Optional[Decimal] = None
    observacoes: Optional[str] = None
    produto_nome: Optional[str] = None
    unidade_nome: Optional[str] = None

    model_config = {"from_attributes": True}


class DemandaResponse(BaseModel):
    """Schema de resposta para demanda"""
    id: int
    organizacao_id: Optional[int] = None
    titulo: str
    descricao: Optional[str] = None
    quantidade: Optional[int] = None
    status: str
    publicada_em: Optional[datetime] = None
    encerra_em: Optional[datetime] = None
    local_entrega_json: Optional[Dict[str, Any]] = None
    criada_por_user_id: int = Field(..., description="ID do usuário que criou a demanda")
    created_at: datetime
    updated_at: datetime
    versao_atual: Optional[int] = None
    versao_atual_id: Optional[int] = None
    itens: List[ItemDemandaResponse] = []

    model_config = {"from_attributes": True}


class ProdutorCapacidadeItem(BaseModel):
    """Item de produção de um produtor"""
    produto_id: int
    produto_nome: str
    unidade_id: int
    unidade_nome: str
    quantidade_disponivel: Optional[Decimal] = None
    preco_base: Optional[Decimal] = None
    capacidade_periodo: Optional[Dict[str, Any]] = None


class ProdutorCapacidadeResponse(BaseModel):
    """Produtor que pode suprir itens da demanda"""
    produtor_id: int
    user_id: int
    nome_produtor: str
    email: str
    tipo_produtor: str
    itens_disponiveis: List[ProdutorCapacidadeItem]
    percentual_cobertura: float = Field(..., description="Percentual de itens da demanda que o produtor pode suprir")
    total_itens_demanda: int
    itens_supriveis: int

