from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class MatchContextInput(BaseModel):
    """Contexto adicional fornecido pelo edital/operador."""

    sazonalidade: Optional[str] = Field(
        default=None,
        description="Informacoes sobre janela de safra, sazonalidade ou restricoes climaticas.",
    )
    urgencia: Optional[str] = Field(
        default=None,
        description="Urgencia percebida do edital: baixa|media|alta.",
    )
    prioridades_edital: List[str] = Field(
        default_factory=list,
        description="Palavras-chave ou prioridades explicitadas (ex: produtos regionais, cooperativas).",
    )
    observacoes: Optional[str] = Field(
        default=None,
        description="Comentarios adicionais que possam influenciar o ajuste de score.",
    )


class CriterionScore(BaseModel):
    score_percentual: float
    peso: float
    contribuicao_percentual: float
    dados_disponiveis: bool = True
    detalhes: Dict[str, Any] = Field(default_factory=dict)


class MatchScoreBreakdown(BaseModel):
    compatibilidade_produto: CriterionScore
    capacidade_entrega: CriterionScore
    historico_sucesso: CriterionScore
    proximidade_geografica: CriterionScore
    tempo_resposta: CriterionScore
    certificacoes: CriterionScore


class MatchScoreRequest(BaseModel):
    versao_demanda_id: int = Field(..., description="Versao da demanda a ser avaliada.")
    produtor_id: int = Field(..., description="Perfil de produtor candidato ao match.")
    contexto: Optional[MatchContextInput] = Field(
        default=None, description="Opcional: contexto adicional para ajuste fino."
    )


class MatchScoreResponse(BaseModel):
    demanda_id: int
    versao_demanda_id: int
    produtor_id: int
    score_percentual: float
    justificativa: str
    pontos_fortes: List[str] = Field(default_factory=list)
    pontos_fracos: List[str] = Field(default_factory=list)
    confianca_percentual: float
    confianca_label: str
    contexto_ajustes: List[str] = Field(default_factory=list)
    breakdown: MatchScoreBreakdown
    pesos_utilizados: Dict[str, float]
    metadados: Dict[str, Any] = Field(default_factory=dict)


class MatchOptionProdutor(BaseModel):
    id: int
    nome: str
    score: float
    quantidade_fornecida: float
    percentual_da_demanda: float
    justificativa: str


class MatchOption(BaseModel):
    tipo: str  # individual | grupo
    score_agregado: float
    produtores: List[MatchOptionProdutor]
    preco_total_estimado: Optional[float] = None
    prazo_entrega_medio: Optional[str] = None


class MatchResultResponse(BaseModel):
    demanda_id: int
    status: str  # match_encontrado | grupo_formado | parcial | sem_match
    cobertura_percentual: float
    opcoes: List[MatchOption]
    alternativas: List[Dict[str, Any]] = Field(default_factory=list)
    substituicoes_sugeridas: List[Dict[str, Any]] = Field(default_factory=list)
