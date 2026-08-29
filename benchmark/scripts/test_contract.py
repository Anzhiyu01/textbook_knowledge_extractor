from __future__ import annotations

import unittest
from pathlib import Path
import sys

SKILL_SCRIPTS = Path(__file__).resolve().parents[2] / "skill" / "textbook-knowledge-extractor" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

from contract import BLOCK_ID_RE, CONTAINER_TYPES, DECISIONS, valid_block_id
from bilingual import _BLOCK_ID_RE


class ContractConsistencyTests(unittest.TestCase):
    def test_block_id_contract_is_shared(self) -> None:
        for value in ("K-001", "K-1018", "K-99999"):
            self.assertTrue(valid_block_id(value))
            self.assertIsNotNone(BLOCK_ID_RE.fullmatch(value))
            self.assertIsNotNone(_BLOCK_ID_RE.search(f"## {value} Definition"))
        self.assertFalse(valid_block_id("K-12"))

    def test_decision_and_container_contracts_are_nonempty(self) -> None:
        self.assertEqual(DECISIONS, {"include", "exclude"})
        self.assertIn("callout", CONTAINER_TYPES)
        self.assertIn("display_formula", CONTAINER_TYPES)

    def test_schema_uses_shared_block_pattern_and_v23(self) -> None:
        schema = (Path(__file__).resolve().parents[1] / "schemas" / "audit.schema.json").read_text(encoding="utf-8")
        self.assertIn('"2.3"', schema)
        self.assertIn('^K-[0-9]{3,}$', schema)


if __name__ == "__main__":
    unittest.main()
