from pydantic import BaseModel, EmailStr
from typing import List, Literal


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
    cpfs: List[str]  # Lista de CPFs dos participantes


class RegisterGrupoFormal(BaseModel):
    """Schema para registro de grupo formal"""
    name: str
    email: EmailStr
    senha: str
    cnpj: str  # Format: XX.XXX.XXX/XXXX-XX


class RegisterRequest(BaseModel):
    """Schema genérico para registro que recebe o tipo de conta"""
    tipo_conta: Literal["fornecedor_individual", "grupo_informal", "grupo_formal"]
    name: str
    email: EmailStr
    senha: str
    cpf: str = None  # Obrigatório para fornecedor_individual e grupo_informal
    cpfs: List[str] = None  # Obrigatório para grupo_informal
    cnpj: str = None  # Obrigatório para grupo_formal
