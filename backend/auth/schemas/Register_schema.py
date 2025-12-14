from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal, Optional
from pydantic import ConfigDict


class Participante(BaseModel):
    """Schema para um participante do grupo informal"""
    nome: Optional[str] = None
    cpf: str

    model_config = ConfigDict(populate_by_name=True)


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
    # Compatibilidade com payload antigo que enviava apenas lista de CPFs
    cpfs: Optional[List[str]] = Field(default=None, alias="cpfs")
    cnpj: Optional[str] = None  # Para grupo_formal
    nome_escola: Optional[str] = None  # Para escola
    nome_orgao: Optional[str] = None  # Para governo
    nivel: Optional[Literal["municipal", "estadual", "federal"]] = None  # Para governo
    endereco: Optional[str] = None  # Para escola ou governo
    telefone: Optional[str] = None  # Para escola ou governo

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        json_schema_extra={
            "examples": [
                {
                    "tipo_usuario": "produtor",
                    "subtipo_usuario": "fornecedor_individual",
                    "name": "João Silva",
                    "email": "joao.silva@example.com",
                    "senha": "senha123",
                    "cpf": "123.456.789-10",
                    "latitude": -22.9068,
                    "longitude": -43.1729
                },
                {
                    "tipo_usuario": "produtor",
                    "subtipo_usuario": "grupo_informal",
                    "name": "Grupo Informal ABC",
                    "email": "grupo.informal@example.com",
                    "senha": "senha123",
                    "participantes": [
                        {"nome": "João Silva", "cpf": "111.111.111-11"},
                        {"nome": "Maria Santos", "cpf": "222.222.222-22"},
                        {"nome": "Pedro Costa", "cpf": "333.333.333-33"}
                    ]
                },
                {
                    "tipo_usuario": "produtor",
                    "subtipo_usuario": "grupo_formal",
                    "name": "Associação de Produtores XYZ",
                    "email": "assoc@example.com",
                    "senha": "senha123",
                    "cnpj": "12.345.678/0001-99"
                },
                {
                    "tipo_usuario": "entidade_executora",
                    "subtipo_usuario": "escola",
                    "name": "Escola Estadual Exemplo",
                    "email": "escola@example.com",
                    "senha": "senha123",
                    "nome_escola": "Escola Estadual ABC",
                    "endereco": "Rua das Flores, 123",
                    "telefone": "(21) 3333-4444"
                },
                {
                    "tipo_usuario": "entidade_executora",
                    "subtipo_usuario": "governo",
                    "name": "Secretaria Municipal",
                    "email": "governo@example.com",
                    "senha": "senha123",
                    "nome_orgao": "Secretaria Municipal de Agricultura",
                    "nivel": "municipal",
                    "endereco": "Av. Principal, 456",
                    "telefone": "(21) 3333-5555"
                }
            ]
        },
    )
