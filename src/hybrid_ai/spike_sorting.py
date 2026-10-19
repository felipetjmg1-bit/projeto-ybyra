"""Detecção básica de picos negativos em um traço MEA; não faz diagnóstico neural."""
from statistics import median
from typing import Sequence


def detect_spikes(signal: Sequence[float], *, threshold_mad: float = 4.0, refractory_samples: int = 2) -> list[int]:
    """Retorna índices de mínimos locais abaixo de mediana - k*MAD escalado.

    É uma demonstração para sinais sintéticos/MEA previamente adquiridos; não é
    um pipeline validado de aquisição, classificação de unidades ou interpretação.
    """
    if threshold_mad <= 0 or refractory_samples < 1:
        raise ValueError("threshold_mad deve ser > 0 e refractory_samples >= 1")
    if len(signal) < 3:
        return []
    center = median(signal)
    mad = median(abs(float(value) - center) for value in signal)
    if mad == 0:
        return []
    cutoff = center - threshold_mad * 1.4826 * mad
    peaks = []
    for i in range(1, len(signal) - 1):
        if signal[i] <= cutoff and signal[i] <= signal[i - 1] and signal[i] < signal[i + 1]:
            if not peaks or i - peaks[-1] >= refractory_samples:
                peaks.append(i)
    return peaks
