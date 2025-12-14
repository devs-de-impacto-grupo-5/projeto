from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import JSONResponse

from models.User_model import User
from schemas.Edital_schema import EditalProcessamentoResponse
from security.security import get_current_user
from services.edital_ai import (
    GeminiAIError,
    GeminiConfigurationError,
    InvalidPDFError,
    PDFExtractionError,
    get_edital_processor,
)

router = APIRouter(prefix="/editais", tags=["RF30 - Editais"])


@router.post(
    "/processar",
    response_model=EditalProcessamentoResponse,
    summary="Processa um edital com autenticacao (gera rascunho vinculado).",
)
async def processar_edital(
    arquivo: UploadFile = File(..., description="Arquivo PDF do edital."),
    organization_id: Optional[int] = Form(
        default=None, description="Identificador da organizacao requisitante."
    ),
    current_user: User = Depends(get_current_user),
):
    """
    Processa o PDF enviado usando o Gemini, gera um rascunho pre-formatado e vincula o usuario autenticado.
    """
    return await _executar_processamento(
        arquivo=arquivo,
        organization_id=organization_id,
        current_user=current_user,
        gerar_rascunho=True,
    )


@router.post(
    "/processar-publico",
    response_model=EditalProcessamentoResponse,
    summary="Processa um edital sem autenticacao (modo publico).",
)
async def processar_edital_publico(
    arquivo: UploadFile = File(..., description="Arquivo PDF do edital."),
    organization_id: Optional[int] = Form(
        default=None, description="Identificador da organizacao, se aplicavel."
    ),
):
    """
    Processa o PDF enviado usando o Gemini sem exigir autenticacao.
    Nao gera um rascunho persistido.
    """
    return await _executar_processamento(
        arquivo=arquivo,
        organization_id=organization_id,
        current_user=None,
        gerar_rascunho=False,
    )


async def _executar_processamento(
    *,
    arquivo: UploadFile,
    organization_id: Optional[int],
    current_user: Optional[User],
    gerar_rascunho: bool,
):
    try:
        processor = get_edital_processor()
    except GeminiConfigurationError as exc:
        return JSONResponse(status_code=500, content={"success": False, "erro": str(exc)})

    try:
        return await processor.process_upload(
            arquivo,
            organization_id=organization_id,
            current_user=current_user,
            gerar_rascunho=gerar_rascunho,
        )
    except InvalidPDFError as exc:
        return JSONResponse(status_code=400, content={"success": False, "erro": str(exc)})
    except PDFExtractionError as exc:
        return JSONResponse(status_code=422, content={"success": False, "erro": str(exc)})
    except GeminiAIError as exc:
        return JSONResponse(status_code=502, content={"success": False, "erro": str(exc)})
