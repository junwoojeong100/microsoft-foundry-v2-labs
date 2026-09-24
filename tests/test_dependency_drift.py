import json
import unittest
from unittest.mock import patch

from . import ROOT
from .test_packaging import load_script

DRIFT = load_script("check_dependency_drift")


class DependencyDriftTests(unittest.TestCase):
    def test_every_pinned_extra_is_reported_without_changing_pins(self):
        pins = DRIFT.pinned_requirements(ROOT)
        self.assertIn("azure-ai-projects", pins)
        self.assertIn("agent-framework-foundry-hosting", pins)
        before = (ROOT / "pyproject.toml").read_bytes()
        latest = {name: version for name, version in pins.items()}
        latest["openai"] = "99.0.0"
        result = DRIFT.report(ROOT, fetch=latest.__getitem__)
        self.assertEqual((ROOT / "pyproject.toml").read_bytes(), before)
        self.assertIs(result["pins_changed"], False)
        self.assertEqual(result["major_drift"], ["openai"])
        self.assertEqual(len(result["packages"]), len(pins))

    def test_classification_covers_patch_minor_major_and_prerelease(self):
        self.assertEqual(DRIFT.classify("2.6.1", "2.6.1"), "current")
        self.assertEqual(DRIFT.classify("2.6.1", "2.6.2"), "patch")
        self.assertEqual(DRIFT.classify("2.6.1", "2.7.0"), "minor")
        self.assertEqual(DRIFT.classify("1.30.0", "2.2.0"), "major")
        self.assertEqual(DRIFT.classify("1.0.0b260910", "1.0.0b260918"), "prerelease")
        self.assertEqual(DRIFT.classify("3.16.1", "3.1.0"), "pinned-newer")

    def test_unreachable_index_is_reported_not_hidden(self):
        def offline(_name):
            raise OSError("network disabled in unit test")

        result = DRIFT.report(ROOT, fetch=offline)
        self.assertEqual(len(result["unavailable"]), len(result["packages"]))
        self.assertTrue(all(item["latest"] is None for item in result["packages"]))
        self.assertIn("unavailable", result["packages"][0]["drift"])

    def test_summary_table_lists_each_package(self):
        with patch.object(DRIFT, "fetch_latest", side_effect=lambda name: "0.0.1"):
            result = DRIFT.report(ROOT, fetch=DRIFT.fetch_latest)
        table = DRIFT.markdown(result)
        for item in result["packages"]:
            self.assertIn(f"`{item['name']}`", table)
        json.dumps(result)
