import json
import os
import re
import secrets
import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Dict, List, Optional

import google.generativeai as genai
import pdfplumber
from dotenv import load_dotenv
from fastapi import UploadFile
from fastapi.concurrency import run_in_threadpool

from db import get_session_local
from models.Documento_model import Arquivo
from models.EditalRascunho_model import ItemRascunho, RascunhoEdital

# Garantir que variaveis do .env estejam carregadas antes de usar os serviços de IA.
load_dotenv()


class InvalidPDFError(Exception):
    """Raised when the uploaded file is not a valid PDF."""


class PDFExtractionError(Exception):
    """Raised when the service cannot extract text from the PDF."""


class GeminiAIError(Exception):
    """Raised when Gemini fails or returns an invalid payload."""


class GeminiConfigurationError(RuntimeError):
    """Raised when Gemini configuration is missing or invalid."""


PDF_MIME_TYPES = {
    "application/pdf",
    "application/x-pdf",
    "application/octet-stream",
}


@dataclass
class ProcessedArquivo:
    nome_original: str
    caminho_absoluto: Path
    caminho_relativo: str
    tamanho_bytes: int


class PDFProcessor:
    def __init__(self, upload_dir: Path, project_root: Path) -> None:
        self.upload_dir = upload_dir
        self.project_root = project_root
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save_upload(self, upload_file: UploadFile) -> ProcessedArquivo:
        self._validate_upload(upload_file)
        filename = self._build_filename(upload_file.filename or "edital.pdf")
        destination = self.upload_dir / filename

        contents = await upload_file.read()
        if not contents:
            raise InvalidPDFError("O arquivo PDF enviado esta vazio.")

        destination.write_bytes(contents)
        await upload_file.seek(0)  # Permite reuso em outros pontos se necessario.

        rel_path = os.path.relpath(destination, self.project_root)
        tamanho_bytes = destination.stat().st_size
        return ProcessedArquivo(
            nome_original=upload_file.filename or "edital.pdf",
            caminho_absoluto=destination,
            caminho_relativo=rel_path,
            tamanho_bytes=tamanho_bytes,
        )

    def extract_text(self, file_path: Path, max_pages: Optional[int] = None) -> str:
        try:
            with pdfplumber.open(str(file_path)) as pdf:
                pages = pdf.pages
                if max_pages:
                    pages = pages[:max_pages]
                text_parts: List[str] = []
                for page in pages:
                    page_text = page.extract_text() or ""
                    if page_text.strip():
                        text_parts.append(page_text.strip())
        except Exception as exc:  # pragma: no cover - pdfplumber internals
            raise PDFExtractionError("Nao foi possivel ler o PDF enviado.") from exc

        combined = "\n".join(text_parts).strip()
        if not combined:
            raise PDFExtractionError("Nenhum texto foi encontrado no PDF enviado.")
        return combined

    @staticmethod
    def _build_filename(original_name: str) -> str:
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        random_suffix = secrets.token_hex(4)
        base = re.sub(r"[^a-zA-Z0-9_-]", "_", Path(original_name).stem).strip("_") or "edital"
        return f"{base[:40]}_{timestamp}_{random_suffix}.pdf"

    @staticmethod
    def _validate_upload(upload_file: UploadFile) -> None:
        mime_type = upload_file.content_type or ""
        is_pdf = mime_type.lower() in PDF_MIME_TYPES or (upload_file.filename or "").lower().endswith(".pdf")
        if not is_pdf:
            raise InvalidPDFError("Envie um arquivo no formato PDF.")


class GeminiClient:
    DEFAULT_MODEL = "gemini-2.5-flash-lite"

    def __init__(self, api_key: str, model_name: Optional[str] = None) -> None:
        if not api_key:
            raise GeminiConfigurationError(
                "Configure a variavel de ambiente GEMINI_API_KEY para habilitar o RF30."
            )

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name or self.DEFAULT_MODEL)
        self._generation_config = {
            "temperature": 0.2,
            "response_mime_type": "application/json",
        }

    def analyze_edital(self, edital_text: str) -> Dict[str, Any]:
        prompt = self._build_prompt(edital_text)
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self._generation_config,
            )
        except Exception as exc:  # pragma: no cover - depends on remote API
            # Include the original exception message to help debugging (no secrets)
            raise GeminiAIError(f"Falha ao consultar o Gemini: {type(exc).__name__}: {str(exc)}") from exc

        raw_text = self._extract_response_text(response)
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError as exc:
            raise GeminiAIError("O Gemini retornou dados fora do formato JSON esperado.") from exc

    @staticmethod
    def _extract_response_text(response: Any) -> str:
        if getattr(response, "text", None):
            return response.text

        candidates = getattr(response, "candidates", []) or []
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            parts = getattr(content, "parts", None)
            if not parts:
                continue
            texts = [getattr(part, "text", "") for part in parts if getattr(part, "text", "")]
            if texts:
                return "\n".join(texts)
        raise GeminiAIError("Resposta do Gemini sem conteudo textual.")

    @staticmethod
    def _build_prompt(edital_text: str) -> str:
        return (
            "Voce e um assistente especialista em editais de compras publicas do PNAE. "
            "Analise o conteudo a seguir e gere um JSON valido com o formato:\n"
            "{\n"
            '  "titulo": "Titulo resumido do edital",\n'
            '  "contexto": "Descricao curta com orgao demandante, regiao e objetivos",\n'
            '  "resumo": "Principais observacoes e prazos",\n'
            '  "confianca_geral": "Alta|Media|Baixa",\n'
            '  "itens": [\n'
            "     {\n"
            '        "produto_nome": "Produto ou grupo solicitado",\n'
            '        "descricao_adicional": "Beneficios, variedade, padroes de qualidade",\n'
            '        "quantidade": "Quantidade numerica quando existir",\n'
            '        "unidade": "Unidade (kg, toneladas, cestas)",\n'
            '        "categoria": "Categoria resumida do item (hortifruti, mercearia, laticinios, proteinas, outros)",\n'
            '        "preco_estimado": "Preco unitario aproximado com moeda (R$)",\n'
            '        "confianca": "Alta|Media|Baixa"\n'
            "     }\n"
            "   ],\n"
            '  "observacoes": "Alertas complementares, como datas ou documentos"\n'
            "}\n"
            "Retorne SOMENTE o JSON solicitado.\n\n"
            f"Texto do edital a analisar:\n\"\"\"\n{edital_text}\n\"\"\""
        )


class EditalProcessor:
    def __init__(
        self,
        upload_dir: Path,
        project_root: Path,
        api_key: str,
        model_name: Optional[str] = None,
        max_chars: int = 18000,
        preview_items: int = 5,
    ) -> None:
        self.pdf_processor = PDFProcessor(upload_dir=upload_dir, project_root=project_root)
        self.gemini_client = GeminiClient(api_key=api_key, model_name=model_name)
        self.max_chars = max_chars
        self.preview_items = preview_items

    async def process_upload(
        self,
        upload_file: UploadFile,
        *,
        organization_id: Optional[int],
        current_user: Optional[Any],
        gerar_rascunho: bool,
    ) -> Dict[str, Any]:
        arquivo_info = await self.pdf_processor.save_upload(upload_file)
        extracted_text = await run_in_threadpool(self.pdf_processor.extract_text, arquivo_info.caminho_absoluto)
        truncated_text = self._truncate_text(extracted_text)
        ai_payload = await run_in_threadpool(self.gemini_client.analyze_edital, truncated_text)
        normalized_payload = self._normalize_payload(ai_payload)

        # Persistir rascunho e arquivo caso solicitado
        db_saved = False
        rascunho_db_id = None
        if gerar_rascunho:
            Session = get_session_local()
            db = Session()
            try:
                arquivo_db = Arquivo(
                    nome_original=arquivo_info.nome_original,
                    caminho_storage=arquivo_info.caminho_relativo,
                    mime_type="application/pdf",
                    tamanho_bytes=arquivo_info.tamanho_bytes,
                    uploaded_by_user_id=getattr(current_user, "id", None),
                )
                db.add(arquivo_db)
                db.flush()

                rascunho = RascunhoEdital(
                    titulo=normalized_payload.get("titulo"),
                    descricao=normalized_payload.get("resumo"),
                    organizacao_id=organization_id,
                    arquivo_id=arquivo_db.id,
                    criada_por_user_id=getattr(current_user, "id", None),
                    conteudo_estruturado_json=normalized_payload,
                )
                db.add(rascunho)
                db.flush()

                itens = normalized_payload.get("itens", [])
                for it in itens:
                    # try to parse price into Decimal for Numeric field
                    preco_val = None
                    try:
                        preco_str = it.get("preco_estimado") or it.get("preco") or it.get("valor")
                        if preco_str:
                            preco_val = self._parse_price(preco_str)
                    except Exception:
                        preco_val = None

                    item_db = ItemRascunho(
                        rascunho_id=rascunho.id,
                        produto_nome=it.get("produto_nome"),
                        descricao_adicional=it.get("descricao_adicional"),
                        quantidade=it.get("quantidade"),
                        unidade=it.get("unidade"),
                        categoria=it.get("categoria"),
                        preco_estimado=preco_val,
                        frequencia=it.get("frequencia"),
                        criterios_observacoes=it.get("criterios_observacoes"),
                        confianca=it.get("confianca"),
                    )
                    db.add(item_db)

                db.commit()
                db_saved = True
                rascunho_db_id = rascunho.id
            except Exception:
                db.rollback()
            finally:
                db.close()

        response = self._build_response(
            normalized_payload=normalized_payload,
            arquivo_info=arquivo_info,
            organization_id=organization_id,
            current_user=current_user,
            gerar_rascunho=gerar_rascunho,
        )

        # Add DB metadata to response when persisted
        if db_saved:
            response["db_saved"] = True
            response["rascunho_db_id"] = rascunho_db_id

        return response

    def _parse_price(self, value: Any) -> Optional[Decimal]:
        if value is None:
            return None
        s = str(value).strip()
        try:
            if "," in s and "." in s and s.rfind(",") > s.rfind("."):
                s = s.replace(".", "").replace(",", ".")
            else:
                s = s.replace(",", "")
            s = re.sub(r"[^0-9.-]", "", s)
            if not s:
                return None
            return Decimal(s)
        except (InvalidOperation, Exception):
            return None

    def _truncate_text(self, text: str) -> str:
        if len(text) <= self.max_chars:
            return text
        return text[: self.max_chars] + "\n\n[conteudo truncado para atender ao limite da IA]"

    def _normalize_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        itens_raw = payload.get("itens") or payload.get("itens_previstos") or []
        itens_normalizados: List[Dict[str, Any]] = []
        for item in itens_raw:
            if not isinstance(item, dict):
                continue
            itens_normalizados.append(
                {
                    "produto_nome": self._clean_product_name(
                        item.get("produto_nome") or item.get("produto") or item.get("nome")
                    ),
                    "descricao_adicional": self._safe_string(
                        item.get("descricao_adicional") or item.get("descricao")
                    ),
                    "categoria": self._safe_string(item.get("categoria") or item.get("tipo")),
                    "quantidade": self._safe_string(item.get("quantidade")),
                    "unidade": self._safe_string(item.get("unidade") or item.get("medida")),
                    "preco_estimado": self._safe_string(
                        item.get("preco_estimado") or item.get("preco") or item.get("valor")
                    ),
                    "criterios_observacoes": self._safe_string(
                        item.get("criterios_observacoes")
                        or item.get("criterios")
                        or item.get("observacoes")
                    ),
                    "confianca": self._safe_string(item.get("confianca") or item.get("confiabilidade")),
                }
            )

        return {
            "titulo": payload.get("titulo") or payload.get("titulo_edital"),
            "contexto": payload.get("contexto"),
            "resumo": payload.get("resumo"),
            "confianca_geral": payload.get("confianca_geral"),
            "observacoes": payload.get("observacoes"),
            "itens": itens_normalizados,
        }

    def _clean_product_name(self, value: Any) -> str:
        """Return only the core product name (remove units, parentheses, dashes, and extras)."""
        raw = self._safe_string(value)
        if not raw:
            return ""

        cleaned = raw.replace("?", "-").replace("?", "-").replace("?", "-")
        cleaned = re.split(r"[-:|/]", cleaned, maxsplit=1)[0]
        cleaned = re.sub(r"\(.*?\)", "", cleaned)
        cleaned = re.sub(
            r"(?:kg|g|gr|mg|l|ml|unidade(?:s)?|cx|caixa|molho|tonelada(?:s)?)\.?",
            "",
            cleaned,
            flags=re.I,
        )
        cleaned = re.sub(r"[^\w\s-]", "", cleaned, flags=re.UNICODE).strip()

        return cleaned.upper()

    def _build_response(
        self,
        *,
        normalized_payload: Dict[str, Any],
        arquivo_info: ProcessedArquivo,
        organization_id: Optional[int],
        current_user: Optional[Any],
        gerar_rascunho: bool,
    ) -> Dict[str, Any]:
        itens = normalized_payload.get("itens", [])
        preview = {
            "titulo": normalized_payload.get("titulo"),
            "contexto": normalized_payload.get("contexto"),
            "resumo": normalized_payload.get("resumo"),
            "itens_preview": itens[: self.preview_items],
        }

        resultado: Dict[str, Any] = {
            "success": True,
            "rascunho_id": self._generate_rascunho_id() if gerar_rascunho else None,
            "confianca_geral": normalized_payload.get("confianca_geral"),
            "num_itens": len(itens),
            "organization_id": organization_id,
            "preview": preview,
            "dados_extraidos": normalized_payload,
            "arquivo_processado": {
                "nome_original": arquivo_info.nome_original,
                "caminho": arquivo_info.caminho_relativo,
                "tamanho_bytes": arquivo_info.tamanho_bytes,
            },
        }

        if current_user:
            resultado["processado_por"] = {
                "id": getattr(current_user, "id", None),
                "nome": getattr(current_user, "name", None),
                "email": getattr(current_user, "email", None),
            }

        return resultado

    @staticmethod
    def _generate_rascunho_id() -> str:
        return uuid.uuid4().hex[:12].upper()

    @staticmethod
    def _safe_string(value: Any) -> str:
        if value is None:
            return ""
        return str(value).strip()


_PROCESSOR_INSTANCE: Optional[EditalProcessor] = None
BASE_DIR = Path(__file__).resolve().parents[1]


def get_edital_processor() -> EditalProcessor:
    global _PROCESSOR_INSTANCE
    if _PROCESSOR_INSTANCE:
        return _PROCESSOR_INSTANCE

    upload_dir_env = os.getenv("PDF_UPLOAD_DIR", "storage/editais")
    upload_dir = Path(upload_dir_env)
    if not upload_dir.is_absolute():
        upload_dir = (BASE_DIR / upload_dir).resolve()

    api_key = os.getenv("GEMINI_API_KEY", "")
    model_name = os.getenv("GEMINI_MODEL_NAME")

    _PROCESSOR_INSTANCE = EditalProcessor(
        upload_dir=upload_dir,
        project_root=BASE_DIR,
        api_key=api_key,
        model_name=model_name,
    )
    return _PROCESSOR_INSTANCE
