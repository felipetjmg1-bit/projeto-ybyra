"""Mapeamento reversível de bytes para bases, para demonstrações de DNA storage.

Isto é um formato digital didático; não inclui síntese, amostras ou protocolo biológico.
"""
from __future__ import annotations

from dataclasses import dataclass

_BITS_TO_BASE = {"00": "A", "01": "C", "10": "G", "11": "T"}
_BASE_TO_BITS = {base: bits for bits, base in _BITS_TO_BASE.items()}


@dataclass(frozen=True)
class EncodedDNA:
    sequence: str
    original_length: int
    parity_symbols: int = 0


def encode_bytes(data: bytes, parity_symbols: int = 0) -> EncodedDNA:
    """Codifica cada par de bits em A/C/G/T; pode acrescentar símbolos RS.

    O exemplo limita um bloco de Reed–Solomon a 255 bytes. Para dados maiores,
    deve-se definir e testar um esquema de blocagem e framing antes de uso real.
    """
    if not isinstance(data, bytes):
        raise TypeError("data deve ser bytes")
    if not 0 <= parity_symbols <= 254:
        raise ValueError("parity_symbols deve estar entre 0 e 254")
    payload = data
    if parity_symbols:
        if len(data) + parity_symbols > 255:
            raise ValueError("payload + paridade deve caber em um bloco de até 255 bytes")
        try:
            from reedsolo import RSCodec
        except ImportError as exc:  # pragma: no cover - depends on installation
            raise RuntimeError("Instale as dependências com: pip install -r requirements.txt") from exc
        payload = bytes(RSCodec(parity_symbols).encode(data))
    bits = "".join(f"{byte:08b}" for byte in payload)
    sequence = "".join(_BITS_TO_BASE[bits[i:i + 2]] for i in range(0, len(bits), 2))
    return EncodedDNA(sequence=sequence, original_length=len(data), parity_symbols=parity_symbols)


def decode_sequence(encoded: EncodedDNA) -> bytes:
    """Decodifica um objeto produzido por :func:`encode_bytes` e valida seu tamanho."""
    if not isinstance(encoded, EncodedDNA):
        raise TypeError("encoded deve ser EncodedDNA com metadados de framing")
    try:
        bits = "".join(_BASE_TO_BITS[base] for base in encoded.sequence.upper())
    except KeyError as exc:
        raise ValueError(f"base inválida: {exc.args[0]!r}") from exc
    if len(bits) % 8:
        raise ValueError("comprimento da sequência não é múltiplo de quatro bases")
    payload = bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))
    if encoded.parity_symbols:
        try:
            from reedsolo import RSCodec
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("Instale as dependências com: pip install -r requirements.txt") from exc
        decoded = RSCodec(encoded.parity_symbols).decode(payload)
        payload = bytes(decoded[0] if isinstance(decoded, tuple) else decoded)
    if len(payload) != encoded.original_length:
        raise ValueError("metadados de framing incompatíveis com o payload decodificado")
    return payload


if __name__ == "__main__":
    sample = encode_bytes(b"Ybyra demo", parity_symbols=8)
    print(sample.sequence)
    print(decode_sequence(sample))
