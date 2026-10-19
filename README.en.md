# Ybyrá Project — Mother Tree

**[Versão em português](README.md)**

> **Status:** early-stage software prototype. This repository does not contain biological hardware, orbital QKD, a real STARK proof, a Drex integration, institutional endorsement, or security validation. The diagrams show concepts and simulated components, not deployed systems. GitHub Actions is not active; a reviewable workflow template is available at [`docs/CI-CD-Deploy.template.yml`](docs/CI-CD-Deploy.template.yml).

Ybyrá is an open-source educational project with local Python demonstrations related to DNA-storage encoding, explainable AI, MEA signal processing, classical BB84 simulation, and Merkle inclusion proofs. The research objective is to explore Brazilian technological capabilities with reproducibility and responsibility. This is not an operating system for biological computation.

The project is thematically related to Brazil's **Plano Brasileiro de Inteligência Artificial (PBIA) 2024–2028**, but is not an official PBIA initiative and has no known government funding or endorsement. See the [MCTI overview](https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/transformacaodigital/plano-brasileiro-de-inteligencia-artificial).

## What is implemented

- `src/dna_storage/b2n_encoder.py`: reversible two-bit-to-base mapping (`00→A`, `01→C`, `10→G`, `11→T`) with optional short-block Reed–Solomon parity. It only handles bytes and strings in memory; it does not synthesize or read DNA.
- `src/dna_storage/crispr_targeting.py`: ranks user-supplied metadata using transparent heuristics. It does not design guides, sequences, vectors, or lab protocols.
- `src/hybrid_ai/aurora_xai_engine.py`: a minimal weighted logistic score with visible feature contributions, not a validated neuro-symbolic model.
- `src/hybrid_ai/spike_sorting.py`: heuristic negative-peak detection for numeric traces; no clinical or organoid interpretation.
- `src/quantum_mesh/qkd_pindorama.py`: a classical BB84 teaching simulation with optional intercept-resend. It does not model photons, hardware, authenticated channels, finite-key security, or an orbital link.
- `src/quantum_mesh/zk_drex_integration.py`: a SHA-256 Merkle inclusion demonstration for fictional data. Merkle inclusion is not zero-knowledge and is not a STARK or a Drex integration.

The Banco Central describes Drex as a pilot/test platform; this repository is not a participant or integration. See the [official BCB page](https://www.bcb.gov.br/estabilidadefinanceira/piloto-drex). QKD has significant deployment and implementation limitations; see the [NSA's discussion](https://www.nsa.gov/Cybersecurity/Quantum-Key-Distribution-QKD-and-Quantum-Cryptography-QC/).

## Research boundaries

No DNA is stored in plants here. No experimental CRISPR work, space-to-ground QKD link, real ZK-STARK, or institutional integration is present. No partnership or endorsement by AEB, Brazil's Ministry of Defence, or the Central Bank is claimed. “Sovereignty” is a research objective, not a technical or legal guarantee.

Company and authorship information provided in the project brief: **Impulso Digital Soluções em I.A. Ltda.**; **Felipe Aquino**, Principal Architect. These attributions have not been independently verified.

## Install and run

Python 3.10+ is required.

```bash
git clone https://github.com/felipetjmg1-bit/projeto-ybyra.git
cd projeto-ybyra
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
PYTHONPATH=. python -m unittest discover -s tests -v
```

The test suite covers encoding round trips, the metadata ranking heuristic, XAI contributions, signal peak detection, BB84 toy simulation, and Merkle proof verification. All nine tests passed locally during publication.

## Documentation and assets

- [Technical architecture](docs/ARCHITECTURE.md)
- [Mathematical models and assumptions](docs/MATHEMATICAL_MODELS.md)
- [Static landing page source](docs/index.html)
- [Diagram sources and illustrations](docs/ASSETS/)

The repository contains a static landing page and starter configuration for Vercel and Netlify, but no hosted site is active. GitHub Pages could not be enabled with the current integration permissions. Vercel, Netlify, and Hugging Face are not connected in this session.

## License

The code is licensed under the [MIT License](LICENSE). “Sovereign” is an objective, not a separate license or guarantee.
