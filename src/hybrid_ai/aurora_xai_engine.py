"""Exemplo mínimo de classificação explicável por contribuições ponderadas.

"Aurora XAI" é o nome do protótipo neste repositório, não um sistema validado.
"""
from dataclasses import dataclass
from math import exp
from typing import Mapping


@dataclass(frozen=True)
class Explanation:
    probability: float
    contributions: dict[str, float]
    threshold: float
    label: bool


def explain_score(features: Mapping[str, float], weights: Mapping[str, float], *, bias: float = 0.0, threshold: float = 0.5) -> Explanation:
    """Calcula sigmoid(bias + Σ feature*weight) e retorna parcelas auditáveis."""
    if not 0.0 < threshold < 1.0:
        raise ValueError("threshold deve estar estritamente entre 0 e 1")
    missing = set(features) - set(weights)
    if missing:
        raise ValueError(f"pesos ausentes para: {', '.join(sorted(missing))}")
    contributions = {key: float(features[key]) * float(weights[key]) for key in features}
    z = float(bias) + sum(contributions.values())
    probability = 1.0 / (1.0 + exp(-max(-700.0, min(700.0, z))))
    return Explanation(probability, contributions, threshold, probability >= threshold)
