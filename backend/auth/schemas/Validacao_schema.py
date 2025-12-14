# schemas/Validacao_schema.py
from pydantic import BaseModel, Field


class ValidacaoCPFCNPJRequest(BaseModel):
    """Schema para validação de CPF ou CNPJ"""
    documento: str = Field(
        ..., 
        description="CPF (formato: XXX.XXX.XXX-XX) ou CNPJ (formato: XX.XXX.XXX/XXXX-XX)",
        examples=["123.456.789-10", "12.345.678/0001-99"]
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "documento": "123.456.789-10"
                },
                {
                    "documento": "12.345.678/0001-99"
                }
            ]
        }
    }


class ValidacaoCPFCNPJResponse(BaseModel):
    """Schema de resposta para validação de CPF ou CNPJ"""
    ja_cadastrado: bool = Field(
        ..., 
        description="True se o CPF ou CNPJ já está cadastrado, False caso contrário"
    )
    documento: str = Field(..., description="CPF ou CNPJ validado")
    tipo: str = Field(..., description="Tipo do documento: 'cpf' ou 'cnpj'")

