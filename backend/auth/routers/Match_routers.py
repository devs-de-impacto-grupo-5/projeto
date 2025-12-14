from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models.Demanda_model import VersaoDemanda
from models.PerfilProdutor_model import PerfilProdutor
from models.User_model import User
from schemas.Match_schema import MatchScoreRequest, MatchScoreResponse, MatchResultResponse
from security.security import get_current_user, get_db
from services.match_scoring import MatchScoringService
from services.match_engine import MatchEngineService

router = APIRouter(prefix="/match", tags=["RF31 - Match Scoring"])


@router.post(
    "/score",
    response_model=MatchScoreResponse,
    status_code=status.HTTP_200_OK,
    summary="Calcula o score de correspondencia produtor x demanda.",
)
def calcular_score_match(
    payload: MatchScoreRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Executa o algoritmo RF-31 utilizando dados reais da demanda (versao) e do produtor.
    Retorna score percentual, justificativa e pontos fortes/fracos.
    """
    versao = db.query(VersaoDemanda).filter(VersaoDemanda.id == payload.versao_demanda_id).first()
    if not versao:
        raise HTTPException(status_code=404, detail="Versao de demanda nao encontrada.")

    produtor = db.query(PerfilProdutor).filter(PerfilProdutor.id == payload.produtor_id).first()
    if not produtor:
        raise HTTPException(status_code=404, detail="Perfil de produtor nao encontrado.")

    service = MatchScoringService(db)
    return service.calculate(versao, produtor, payload.contexto)


@router.post(
    "/execute/{versao_demanda_id}",
    response_model=MatchResultResponse,
    status_code=status.HTTP_200_OK,
    summary="Executa RF-14: Match Automático para uma demanda",
)
def executar_match_automatico(
    versao_demanda_id: int,
    trigger: str = "manual_api",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Aciona o motor de match (RF-14) para encontrar produtores ou grupos
    capazes de atender a versão da demanda especificada.
    """
    service = MatchEngineService(db)
    # Validar permissões se necessário (apenas governo/admin?)
    return service.execute_match(versao_demanda_id, trigger=trigger)
