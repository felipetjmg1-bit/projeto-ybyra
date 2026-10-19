"""Demonstração Merkle para dados fictícios; não é ZK-STARK nem integração Drex."""
from __future__ import annotations
import hashlib


def _hash(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def _leaf(value: bytes) -> bytes:
    return _hash(b"\x00" + value)


def _parent(left: bytes, right: bytes) -> bytes:
    return _hash(b"\x01" + left + right)


def merkle_root(values: list[bytes]) -> str:
    if not values:
        raise ValueError("a árvore exige pelo menos uma folha")
    level = [_leaf(value) for value in values]
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [_parent(level[i], level[i + 1]) for i in range(0, len(level), 2)]
    return level[0].hex()


def inclusion_proof(values: list[bytes], index: int) -> tuple[str, list[tuple[str, str]]]:
    """Retorna raiz e lista de (lado_do_irmão, hash_hex) para fins didáticos."""
    if not values or not 0 <= index < len(values):
        raise ValueError("índice inválido ou lista vazia")
    level = [_leaf(value) for value in values]
    proof: list[tuple[str, str]] = []
    position = index
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        sibling = position ^ 1
        proof.append(("left" if sibling < position else "right", level[sibling].hex()))
        level = [_parent(level[i], level[i + 1]) for i in range(0, len(level), 2)]
        position //= 2
    return level[0].hex(), proof


def verify_inclusion(value: bytes, proof: list[tuple[str, str]], expected_root: str) -> bool:
    current = _leaf(value)
    try:
        for side, sibling_hex in proof:
            sibling = bytes.fromhex(sibling_hex)
            if side == "left":
                current = _parent(sibling, current)
            elif side == "right":
                current = _parent(current, sibling)
            else:
                return False
        return current.hex() == expected_root.lower()
    except (ValueError, TypeError):
        return False
