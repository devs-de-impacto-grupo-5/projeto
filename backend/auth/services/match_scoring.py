import json
import math
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from models.Contrato_model import Contrato
from models.Demanda_model import VersaoDemanda
from models.Documento_model import DocumentoProdutor
from models.PerfilProdutor_model import PerfilProdutor
from models.Producao_model import ItemProducao
from models.Proposta_model import ConfirmacaoParticipante, Proposta
from schemas.Match_schema import MatchContextInput


@dataclass
class CriterionResult:
    key: str
    label: str
    weight: float
    score: float = 0.0
    available: bool = False
    details: Dict[str, float] = field(default_factory=dict)

    @property
    def contribution(self) -> float:
        return self.score * self.weight


class MatchScoringService:
    """Calcula o score de correspondencia entre um produtor e uma demanda."""

    FIELD_MAP = {
        "produto": "compatibilidade_produto",
        "capacidade": "capacidade_entrega",
        "historico": "historico_sucesso",
        "proximidade": "proximidade_geografica",
        "tempo_resposta": "tempo_resposta",
        "certificacoes": "certificacoes",
    }

    def __init__(self, db: Session):
        self.db = db

    def calculate(
        self,
        versao_demanda: VersaoDemanda,
        produtor: PerfilProdutor,
        contexto: Optional[MatchContextInput] = None,
    ) -> Dict[str, object]:
        criterios = self._build_base_criterios()

        demanda_itens = versao_demanda.itens or []
        itens_produtor = produtor.itens_producao or []

        criterios["produto"].score, criterios["produto"].available, criterios["produto"].details = (
            self._score_produtos(demanda_itens, itens_produtor)
        )
        criterios["capacidade"].score, criterios["capacidade"].available, criterios["capacidade"].details = (
            self._score_capacidade(demanda_itens, itens_produtor)
        )
        criterios["historico"].score, criterios["historico"].available, criterios["historico"].details = (
            self._score_historico(produtor.id)
        )
        criterios["proximidade"].score, criterios["proximidade"].available, criterios["proximidade"].details = (
            self._score_proximidade(versao_demanda, produtor)
        )
        criterios["tempo_resposta"].score, criterios["tempo_resposta"].available, criterios["tempo_resposta"].details = (
            self._score_tempo_resposta(produtor.id)
        )
        criterios["certificacoes"].score, criterios["certificacoes"].available, criterios["certificacoes"].details = (
            self._score_certificacoes(produtor)
        )

        base_score = sum(crit.contribution for crit in criterios.values())
        contexto_ajustes_valor, contexto_notas = self._aplicar_contexto(contexto, criterios)
        total_score = max(0.0, min(1.0, base_score + contexto_ajustes_valor))

        confidence = self._calcular_confianca(criterios)
        justification = self._build_justificativa(criterios, total_score)
        strengths = self._build_pontos_fortes(criterios)
        weaknesses = self._build_pontos_fracos(criterios)

        breakdown = {
            self.FIELD_MAP[key]: {
                "score_percentual": round(crit.score * 100, 2),
                "peso": crit.weight,
                "contribuicao_percentual": round(crit.contribution * 100, 2),
                "dados_disponiveis": crit.available,
                "detalhes": crit.details,
            }
            for key, crit in criterios.items()
        }

        return {
            "demanda_id": versao_demanda.demanda_id,
            "versao_demanda_id": versao_demanda.id,
            "produtor_id": produtor.id,
            "score_percentual": round(total_score * 100, 2),
            "justificativa": justification,
            "pontos_fortes": strengths,
            "pontos_fracos": weaknesses,
            "confianca_percentual": round(confidence * 100, 2),
            "confianca_label": self._confidence_label(confidence),
            "contexto_ajustes": contexto_notas,
            "breakdown": breakdown,
            "pesos_utilizados": {self.FIELD_MAP[k]: crit.weight for k, crit in criterios.items()},
            "metadados": {
                "itens_demanda": len(demanda_itens),
                "itens_produtor": len(itens_produtor),
                "contexto_fornecido": bool(contexto),
            },
        }

    # --- Scoring helpers -------------------------------------------------

    def _build_base_criterios(self) -> Dict[str, CriterionResult]:
        return {
            "produto": CriterionResult("produto", "Compatibilidade de produto", 0.28),
            "capacidade": CriterionResult("capacidade", "Capacidade de entrega", 0.22),
            "historico": CriterionResult("historico", "Historico de sucesso", 0.18),
            "proximidade": CriterionResult("proximidade", "Proximidade geografica", 0.12),
            "tempo_resposta": CriterionResult("tempo_resposta", "Tempo medio de resposta", 0.10),
            "certificacoes": CriterionResult("certificacoes", "Certificacoes e selos", 0.10),
        }

    def _score_produtos(
        self, demanda_itens, itens_produtor: List[ItemProducao]
    ) -> Tuple[float, bool, Dict[str, float]]:
        demand_products = {item.produto_id for item in demanda_itens if getattr(item, "produto_id", None)}
        producer_products = {item.produto_id for item in itens_produtor if getattr(item, "produto_id", None)}

        if not demand_products:
            return 0.0, False, {"total_itens_demanda": 0, "itens_cobertos": 0}
        if not producer_products:
            return 0.0, False, {"total_itens_demanda": len(demand_products), "itens_cobertos": 0}

        matched = len(demand_products.intersection(producer_products))
        score = matched / len(demand_products)
        details = {"total_itens_demanda": len(demand_products), "itens_cobertos": matched}
        return score, True, details

    def _score_capacidade(
        self, demanda_itens, itens_produtor: List[ItemProducao]
    ) -> Tuple[float, bool, Dict[str, float]]:
        demanda_por_produto: Dict[int, float] = {}
        for item in demanda_itens:
            if not getattr(item, "produto_id", None):
                continue
            demanda_por_produto[item.produto_id] = demanda_por_produto.get(item.produto_id, 0.0) + self._as_float(
                getattr(item, "quantidade", 0)
            )

        capacidade_produtor: Dict[int, float] = {}
        for item in itens_produtor:
            if not getattr(item, "produto_id", None):
                continue
            total_cap = 0.0
            for periodo in getattr(item, "periodos_capacidade", []) or []:
                total_cap += self._as_float(getattr(periodo, "quantidade_capacidade", 0))
            if total_cap > 0:
                capacidade_produtor[item.produto_id] = capacidade_produtor.get(item.produto_id, 0.0) + total_cap

        demanda_total = sum(demanda_por_produto.values())
        if not demanda_total:
            return 0.0, False, {
                "quantidade_demandada": 0.0,
                "quantidade_coberta": 0.0,
            }

        if not capacidade_produtor:
            fallback = 0.4 if itens_produtor else 0.0
            return fallback, False, {
                "quantidade_demandada": round(demanda_total, 2),
                # Sem capacidade declarada, assume cobrir a demanda para fins de match inicial
                "quantidade_coberta": round(demanda_total, 2),
            }

        cobertura = 0.0
        for produto_id, qtd_demanda in demanda_por_produto.items():
            cobertura += min(qtd_demanda, capacidade_produtor.get(produto_id, 0.0))
        score = min(1.0, cobertura / demanda_total) if demanda_total else 0.0
        return score, True, {
            "quantidade_demandada": round(demanda_total, 2),
            "quantidade_coberta": round(cobertura, 2),
        }

    def _score_historico(self, produtor_id: int) -> Tuple[float, bool, Dict[str, float]]:
        total_propostas = (
            self.db.query(Proposta.id)
            .filter(Proposta.produtor_id == produtor_id)
            .count()
        )
        contratos_sucesso = (
            self.db.query(Contrato.id)
            .join(Proposta, Proposta.id == Contrato.proposta_id)
            .filter(
                Proposta.produtor_id == produtor_id,
                Contrato.status.in_(["generated", "signed"]),
            )
            .count()
        )
        if not total_propostas:
            return 0.35, False, {"total_propostas": 0, "contratos_fechados": 0}

        score = contratos_sucesso / total_propostas if total_propostas else 0.0
        return score, True, {
            "total_propostas": total_propostas,
            "contratos_fechados": contratos_sucesso,
        }

    def _score_proximidade(
        self, versao_demanda: VersaoDemanda, produtor: PerfilProdutor
    ) -> Tuple[float, bool, Dict[str, float]]:
        demanda_coords = self._extract_coords(getattr(versao_demanda.demanda, "local_entrega_json", None))
        produtor_coords = self._get_produtor_coords(produtor)
        if not demanda_coords or not produtor_coords:
            return 0.5, False, {"distancia_km": None}

        distancia = self._haversine(demanda_coords, produtor_coords)
        if distancia <= 50:
            score = 1.0
        elif distancia <= 150:
            score = 0.85
        elif distancia <= 300:
            score = 0.65
        elif distancia <= 600:
            score = 0.45
        else:
            score = 0.25
        return score, True, {"distancia_km": round(distancia, 1)}

    def _score_tempo_resposta(self, produtor_id: int) -> Tuple[float, bool, Dict[str, float]]:
        confirmacoes = (
            self.db.query(ConfirmacaoParticipante)
            .filter(
                ConfirmacaoParticipante.produtor_id == produtor_id,
                ConfirmacaoParticipante.respondido_em.isnot(None),
                ConfirmacaoParticipante.convidado_em.isnot(None),
            )
            .all()
        )
        if not confirmacoes:
            return 0.5, False, {"tempo_medio_horas": None}

        total_horas = 0.0
        for conf in confirmacoes:
            delta = conf.respondido_em - conf.convidado_em
            total_horas += max(delta.total_seconds(), 0) / 3600.0
        media = total_horas / len(confirmacoes)
        score = max(0.0, min(1.0, 1 - (media / 168)))  # 7 dias como limite inferior
        return score, True, {"tempo_medio_horas": round(media, 1)}

    def _score_certificacoes(self, produtor: PerfilProdutor) -> Tuple[float, bool, Dict[str, float]]:
        documentos = (
            self.db.query(DocumentoProdutor)
            .filter(DocumentoProdutor.produtor_id == produtor.id)
            .all()
        )
        if not documentos:
            fallback = 0.4 if produtor.status_perfil == "complete" else 0.25
            return fallback, False, {"documentos_avaliados": 0, "documentos_aprovados": 0}

        aprovados = sum(1 for doc in documentos if doc.status == "approved")
        score = aprovados / len(documentos) if documentos else 0.0
        return score, True, {
            "documentos_avaliados": len(documentos),
            "documentos_aprovados": aprovados,
        }

    # --- Context and qualitative helpers --------------------------------

    def _aplicar_contexto(
        self,
        contexto: Optional[MatchContextInput],
        criterios: Dict[str, CriterionResult],
    ) -> Tuple[float, List[str]]:
        if not contexto:
            return 0.0, []

        ajuste = 0.0
        notas: List[str] = []
        tempo = criterios["tempo_resposta"].score
        proximidade = criterios["proximidade"].score
        capacidade = criterios["capacidade"].score

        if contexto.urgencia:
            urg = contexto.urgencia.lower()
            if urg == "alta":
                if tempo >= 0.75:
                    ajuste += 0.02
                    notas.append("Bonus por boa resposta frente a urgencia alta.")
                else:
                    ajuste -= 0.03
                    notas.append("Penalidade: urgencia alta e tempo de resposta moderado.")
            elif urg == "baixa" and tempo >= 0.5:
                ajuste += 0.01
                notas.append("Urgencia baixa libera pequeno bonus.")

        if contexto.sazonalidade:
            saz = contexto.sazonalidade.lower()
            if "safra" in saz and capacidade >= 0.6:
                ajuste += 0.015
                notas.append("Capacidade aderente a janela de safra informada.")
            elif "entressafra" in saz and capacidade < 0.5:
                ajuste -= 0.015
                notas.append("Risco de capacidade em periodo de entressafra.")

        if contexto.prioridades_edital:
            prioridades = [p.lower() for p in contexto.prioridades_edital]
            if any("regional" in p for p in prioridades):
                if proximidade >= 0.7:
                    ajuste += 0.02
                    notas.append("Bonus por proximidade alinhada a prioridade regional.")
                else:
                    ajuste -= 0.02
                    notas.append("Penalidade: prioridade regional sem proximidade suficiente.")
            if any("certificacao" in p for p in prioridades):
                cert = criterios["certificacoes"].score
                if cert < 0.5:
                    ajuste -= 0.02
                    notas.append("Prioridade por certificacoes nao atendida.")

        return ajuste, notas

    def _calcular_confianca(self, criterios: Dict[str, CriterionResult]) -> float:
        disponiveis = sum(1 for crit in criterios.values() if crit.available)
        base = disponiveis / len(criterios)
        media_scores = (
            sum(crit.score for crit in criterios.values() if crit.available) / disponiveis
            if disponiveis
            else 0.5
        )
        confianca = (base * 0.7) + (media_scores * 0.3)
        return max(0.2, min(1.0, confianca))

    def _confidence_label(self, confidence: float) -> str:
        if confidence >= 0.8:
            return "alta"
        if confidence >= 0.55:
            return "media"
        return "baixa"

    def _build_justificativa(
        self,
        criterios: Dict[str, CriterionResult],
        total_score: float,
    ) -> str:
        ordered = sorted(criterios.values(), key=lambda c: c.contribution, reverse=True)
        destaque = ordered[:2]
        partes = [f"Score combinado de {round(total_score * 100, 1)}%."]
        if destaque:
            detalhes = [
                f"{item.label.lower()} ({round(item.score * 100, 0)}% de desempenho)"
                for item in destaque
                if item.score > 0
            ]
            if detalhes:
                partes.append("Destaques: " + ", ".join(detalhes) + ".")

        fraco = next((crit for crit in ordered[::-1] if crit.score < 0.55), None)
        if fraco:
            partes.append(f"Atenção para {fraco.label.lower()} ({round(fraco.score * 100, 0)}%).")
        return " ".join(partes)

    def _build_pontos_fortes(self, criterios: Dict[str, CriterionResult]) -> List[str]:
        pontos: List[str] = []
        for key, crit in criterios.items():
            if crit.score < 0.7:
                continue
            if key == "produto":
                total = int(crit.details.get("total_itens_demanda", 0))
                cobertos = int(crit.details.get("itens_cobertos", 0))
                pontos.append(f"Cobre {cobertos}/{total} itens previstos no edital.")
            elif key == "capacidade":
                pontos.append(
                    f"Capacidade declarada cobre {crit.details.get('quantidade_coberta', 0)} das {crit.details.get('quantidade_demandada', 0)} unidades previstas."
                )
            elif key == "historico":
                pontos.append(f"Ja participou de {crit.details.get('total_propostas', 0)} propostas com {crit.details.get('contratos_fechados', 0)} contratos firmados.")
            elif key == "proximidade" and crit.details.get("distancia_km") is not None:
                pontos.append(f"Distancia aproximada de {crit.details['distancia_km']} km do ponto de entrega.")
            elif key == "tempo_resposta" and crit.details.get("tempo_medio_horas") is not None:
                pontos.append(f"Tempo medio de resposta de {crit.details['tempo_medio_horas']} h.")
            elif key == "certificacoes":
                pontos.append(
                    f"{crit.details.get('documentos_aprovados', 0)} certificacoes/documentos aprovados ativos."
                )
        return pontos

    def _build_pontos_fracos(self, criterios: Dict[str, CriterionResult]) -> List[str]:
        pontos: List[str] = []
        for key, crit in criterios.items():
            if crit.score >= 0.55 and crit.available:
                continue
            if not crit.available:
                pontos.append(f"Sem dados suficientes para {crit.label.lower()}.")
                continue

            if key == "capacidade":
                pontos.append("Capacidade declarada nao cobre toda a demanda.")
            elif key == "proximidade":
                pontos.append("Distancia elevada pode elevar custos logisticos.")
            elif key == "tempo_resposta":
                pontos.append("Tempo medio de resposta acima do desejado.")
            elif key == "certificacoes":
                pontos.append("Certificacoes/selos pendentes ou insuficientes.")
            elif key == "historico":
                pontos.append("Historico de contratos ainda limitado.")
            elif key == "produto":
                pontos.append("Parte dos itens solicitados nao esta no portifolio informado.")
        return pontos

    # --- Utilities -------------------------------------------------------

    def _extract_coords(self, payload) -> Optional[Tuple[float, float]]:
        if not payload:
            return None
        data = payload
        if isinstance(payload, str):
            try:
                data = json.loads(payload)
            except json.JSONDecodeError:
                return None

        if not isinstance(data, dict):
            return None

        candidates = [
            data,
            data.get("coords") if isinstance(data.get("coords"), dict) else None,
            data.get("geo") if isinstance(data.get("geo"), dict) else None,
        ]
        for candidate in candidates:
            if not isinstance(candidate, dict):
                continue
            lat = candidate.get("lat") or candidate.get("latitude")
            lon = candidate.get("lng") or candidate.get("lon") or candidate.get("longitude")
            if lat is not None and lon is not None:
                return float(lat), float(lon)
        return None

    def _get_produtor_coords(self, produtor: PerfilProdutor) -> Optional[Tuple[float, float]]:
        user = getattr(produtor, "user", None)
        if user and getattr(user, "latitude", None) is not None and getattr(user, "longitude", None) is not None:
            return float(user.latitude), float(user.longitude)
        return self._extract_coords(getattr(produtor, "endereco_json", None))

    def _haversine(self, coord_a: Tuple[float, float], coord_b: Tuple[float, float]) -> float:
        lat1, lon1 = math.radians(coord_a[0]), math.radians(coord_a[1])
        lat2, lon2 = math.radians(coord_b[0]), math.radians(coord_b[1])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return 6371 * c

    def _as_float(self, value) -> float:
        if value is None:
            return 0.0
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, datetime):
            return 0.0
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0
