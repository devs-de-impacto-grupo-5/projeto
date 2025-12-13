from pydantic import BaseModel, EmailStr
from typing import List, Literal, Optional


class Participante(BaseModel):
    """Schema para um participante do grupo informal"""
    nome: str
    cpf: str


class RegisterFornecedorIndividual(BaseModel):
    """Schema para registro de fornecedor individual"""
    name: str
    email: EmailStr
    senha: str
    cpf: str  # Format: XXX.XXX.XXX-XX


class RegisterGrupoInformal(BaseModel):
    """Schema para registro de grupo informal"""
    name: str
    email: EmailStr
    senha: str
    participantes: List[Participante]  # Lista de participantes com nome e CPF


class RegisterGrupoFormal(BaseModel):
    """Schema para registro de grupo formal"""
    name: str
    email: EmailStr
    senha: str
    cnpj: str  # Format: XX.XXX.XXX/XXXX-XX


class RegisterEscola(BaseModel):
    """Schema para registro de escola (entidade executora)"""
    name: str
    email: EmailStr
    senha: str
    nome_escola: str
    endereco: Optional[str] = None
    telefone: Optional[str] = None


class RegisterGoverno(BaseModel):
    """Schema para registro de órgão governamental (entidade executora)"""
    name: str
    email: EmailStr
    senha: str
    nome_orgao: str
    nivel: Literal["municipal", "estadual", "federal"]
    endereco: Optional[str] = None
    telefone: Optional[str] = None


class RegisterRequest(BaseModel):
    """Schema genérico para registro que recebe o tipo de conta"""
    # Tipo principal: "produtor" ou "entidade_executora"
    tipo_usuario: Literal["produtor", "entidade_executora"]

    # Subtipo específico
    # Para produtor: "fornecedor_individual", "grupo_informal", "grupo_formal"
    # Para entidade_executora: "escola", "governo"
    subtipo_usuario: Literal[
        "fornecedor_individual",
        "grupo_informal",
        "grupo_formal",
        "escola",
        "governo"
    ]

    # Dados obrigatórios
    name: str
    email: EmailStr
    senha: str

    # Localização (coordenadas GPS) - Opcionais
    latitude: Optional[float] = None  # -90 a 90
    longitude: Optional[float] = None  # -180 a 180

    # Dados específicos por tipo (opcionais conforme o tipo)
    cpf: Optional[str] = None  # Para fornecedor_individual
    participantes: Optional[List[Participante]] = None  # Para grupo_informal
    cnpj: Optional[str] = None  # Para grupo_formal
    nome_escola: Optional[str] = None  # Para escola
    nome_orgao: Optional[str] = None  # Para governo
    nivel: Optional[Literal["municipal", "estadual", "federal"]] = None  # Para governo
    endereco: Optional[str] = None  # Para escola ou governo
    telefone: Optional[str] = None  # Para escola ou governo
