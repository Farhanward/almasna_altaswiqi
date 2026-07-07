from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from almasna_altaswiqi.batch import evaluate
from almasna_altaswiqi.core import content_brief
from almasna_altaswiqi.datasets import convert_tweet_eval


class AlMasnaTests(unittest.TestCase):
    def test_content_brief(self):
        brief = content_brief("fast simple automation saves time for teams", brand="CarbonFlow")
        self.assertIn("CarbonFlow", brief["title"])
        self.assertTrue(brief["keywords"])
        self.assertGreaterEqual(len(brief["outline"]), 4)

    def test_convert_and_batch_fixture(self):
        with tempfile.TemporaryDirectory(dir="C:/Projects") as tmp:
            source = Path(tmp) / "tweets.jsonl"
            out = Path(tmp) / "marketing.jsonl"
            source.write_text('{"text":"fast tool saves time","label":2,"success":true}\n{"text":"bad problem fail","label":0,"success":false}\n', encoding="utf-8")
            info = convert_tweet_eval(source, out)
            self.assertEqual(info["rows"], 2)
            summary = evaluate(out)
            self.assertEqual(summary["errors"], 0)
            self.assertEqual(summary["complete"], 2)


if __name__ == "__main__":
    unittest.main()

