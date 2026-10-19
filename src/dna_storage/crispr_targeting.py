"""Priorização de candidatos por metadados declarados, sem desenho experimental.

Não pontua sequências nem projeta guias CRISPR. Os escores são heurísticos e não
constituem recomendação para edição genética, contenção ou trabalho de bancada.
"""
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class LocusCandidate:
    name: str
    compartment: str  # "nuclear", "chloroplast", or "unknown"
    heterochromatin_score: float  # metadata supplied by caller, in [0, 1]
    expression_risk: float  # caller-estimated risk, in [0, 1]
    off_target_risk: float  # caller-estimated risk, in [0, 1]
    evidence_level: str = "unvalidated"


def rank_candidates(candidates: Iterable[LocusCandidate]) -> list[tuple[LocusCandidate, float]]:
    """Ordena metadados de candidatos por um escore transparente e não biológico."""
    ranked = []
    for item in candidates:
        values = (item.heterochromatin_score, item.expression_risk, item.off_target_risk)
        if any(not 0.0 <= value <= 1.0 for value in values):
            raise ValueError("todos os escores devem estar no intervalo [0, 1]")
        compartment_prior = 0.10 if item.compartment == "chloroplast" else 0.0
        score = (
            0.45 * item.heterochromatin_score
            + compartment_prior
            + 0.25 * (1.0 - item.expression_risk)
            + 0.30 * (1.0 - item.off_target_risk)
        )
        ranked.append((item, min(score, 1.0)))
    return sorted(ranked, key=lambda pair: pair[1], reverse=True)
