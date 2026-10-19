"""Simulação clássica didática de BB84; não implementa óptica nem QKD operacional."""
from dataclasses import dataclass
import random


@dataclass(frozen=True)
class QKDResult:
    rounds: int
    sifted_bits: int
    qber: float
    detected: bool
    alice_key: tuple[int, ...]
    bob_key: tuple[int, ...]


def simulate_bb84(rounds: int = 1000, *, eve_intercepts: bool = False, threshold: float = 0.11, seed: int | None = None) -> QKDResult:
    """Simula preparação/medição BB84 em bits e bases, com Eve opcional.

    O simulador serve para ensino e testes. Não modela canal óptico, perdas,
    detector, autenticação clássica, finite-key bounds nem segurança comprovada.
    """
    if rounds < 1:
        raise ValueError("rounds deve ser >= 1")
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold deve estar entre 0 e 1")
    rng = random.Random(seed)
    alice_bits = [rng.randrange(2) for _ in range(rounds)]
    alice_bases = [rng.randrange(2) for _ in range(rounds)]
    bob_bases = [rng.randrange(2) for _ in range(rounds)]
    bob_bits = []
    for i in range(rounds):
        if eve_intercepts:
            eve_basis = rng.randrange(2)
            eve_bit = alice_bits[i] if eve_basis == alice_bases[i] else rng.randrange(2)
            bob_bits.append(eve_bit if bob_bases[i] == eve_basis else rng.randrange(2))
        else:
            bob_bits.append(alice_bits[i] if bob_bases[i] == alice_bases[i] else rng.randrange(2))
    matched = [i for i in range(rounds) if alice_bases[i] == bob_bases[i]]
    alice_key = tuple(alice_bits[i] for i in matched)
    bob_key = tuple(bob_bits[i] for i in matched)
    qber = sum(a != b for a, b in zip(alice_key, bob_key)) / len(matched) if matched else 0.0
    return QKDResult(rounds, len(matched), qber, qber > threshold, alice_key, bob_key)
