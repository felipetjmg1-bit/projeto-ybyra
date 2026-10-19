import unittest

from src.dna_storage.b2n_encoder import decode_sequence, encode_bytes
from src.dna_storage.crispr_targeting import LocusCandidate, rank_candidates
from src.hybrid_ai.aurora_xai_engine import explain_score
from src.hybrid_ai.spike_sorting import detect_spikes
from src.quantum_mesh.qkd_pindorama import simulate_bb84
from src.quantum_mesh.zk_drex_integration import inclusion_proof, verify_inclusion


class DnaEncodingTests(unittest.TestCase):
    def test_round_trip_without_parity(self):
        encoded = encode_bytes(b"Ybyra")
        self.assertEqual(len(encoded.sequence), 20)
        self.assertEqual(decode_sequence(encoded), b"Ybyra")

    def test_round_trip_with_reed_solomon_parity(self):
        encoded = encode_bytes(b"small test", parity_symbols=8)
        corrupted = list(encoded.sequence)
        corrupted[2] = "A" if corrupted[2] != "A" else "C"
        from dataclasses import replace
        self.assertEqual(decode_sequence(replace(encoded, sequence="".join(corrupted))), b"small test")

    def test_bad_base_rejected(self):
        from dataclasses import replace
        encoded = encode_bytes(b"x")
        with self.assertRaises(ValueError):
            decode_sequence(replace(encoded, sequence="AXAA"))


class MetadataAndXaiTests(unittest.TestCase):
    def test_locus_ranking_prefers_lower_risk_candidate(self):
        items = [
            LocusCandidate("a", "nuclear", 0.8, 0.7, 0.8),
            LocusCandidate("b", "chloroplast", 0.7, 0.1, 0.1),
        ]
        self.assertEqual(rank_candidates(items)[0][0].name, "b")

    def test_explanation_sums_contributions(self):
        result = explain_score({"x": 2.0, "y": -1.0}, {"x": 0.5, "y": 1.0}, bias=0.0)
        self.assertAlmostEqual(result.probability, 0.5)
        self.assertEqual(result.contributions, {"x": 1.0, "y": -1.0})

    def test_spike_detection(self):
        signal = [0, 0.1, -0.1, 0.1, 0, -8, 0.1, 0, 0.1, 0, 0.2]
        self.assertEqual(detect_spikes(signal, threshold_mad=2.0), [5])


class QuantumAndMerkleTests(unittest.TestCase):
    def test_bb84_without_eve(self):
        result = simulate_bb84(rounds=2000, seed=2)
        self.assertGreater(result.sifted_bits, 0)
        self.assertEqual(result.qber, 0.0)
        self.assertFalse(result.detected)

    def test_bb84_intercept_resend_increases_qber(self):
        result = simulate_bb84(rounds=5000, eve_intercepts=True, seed=22)
        self.assertGreater(result.qber, 0.11)
        self.assertTrue(result.detected)

    def test_merkle_inclusion_and_tamper_detection(self):
        values = [b"record-0", b"record-1", b"record-2"]
        root, proof = inclusion_proof(values, 1)
        self.assertTrue(verify_inclusion(values[1], proof, root))
        self.assertFalse(verify_inclusion(b"changed", proof, root))


if __name__ == "__main__":
    unittest.main()
