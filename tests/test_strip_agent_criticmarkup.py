#!/usr/bin/env python3
"""Unit tests for manuscript-collab agent CriticMarkup stripper."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/manuscript-collab/scripts/strip_agent_criticmarkup.py"
FIXTURE = ROOT / "tests/fixtures/criticmarkup_mixed.md"


def load_mod():
    spec = importlib.util.spec_from_file_location("strip_agent_criticmarkup", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


class TestStripAgentCriticmarkup(unittest.TestCase):
    def setUp(self) -> None:
        self.mod = load_mod()

    def test_keeps_human_comment(self) -> None:
        src = "Hello.{>>@Ada Lee (2025-09-09 22:21) | Please expand.<<}"
        out, stats = self.mod.strip_agent_comments(src)
        self.assertEqual(out, src)
        self.assertEqual(sum(stats.values()), 0)

    def test_strips_at_claude(self) -> None:
        src = "Hello.{>>@Claude | provenance note<<} World"
        out, stats = self.mod.strip_agent_comments(src)
        self.assertEqual(out, "Hello. World")
        self.assertGreaterEqual(stats.get("Claude", 0), 1)

    def test_strips_claude_date_without_at(self) -> None:
        src = "X.{>>Claude (2026-07-21) | Provenance: seed=42.<<}Y"
        out, stats = self.mod.strip_agent_comments(src)
        self.assertEqual(out, "X.Y")
        self.assertGreaterEqual(stats.get("Claude", 0), 1)

    def test_unwraps_paired_highlight(self) -> None:
        src = "{==Introduction==}{>>@Claude | fix heading<<}"
        out, stats = self.mod.strip_agent_comments(src)
        self.assertEqual(out, "Introduction")
        self.assertGreaterEqual(sum(stats.values()), 1)

    def test_keeps_standalone_highlight(self) -> None:
        src = "See {==important==} claim."
        out, stats = self.mod.strip_agent_comments(src)
        self.assertEqual(out, src)
        self.assertEqual(sum(stats.values()), 0)

    def test_keeps_track_changes(self) -> None:
        src = "A {++added++} B {--deleted--} C {~~old~>new~~}"
        out, stats = self.mod.strip_agent_comments(src)
        self.assertEqual(out, src)

    def test_composer_alias_as_cursor(self) -> None:
        src = "Note.{>>@Composer | agent note<<}"
        out, stats = self.mod.strip_agent_comments(src)
        self.assertEqual(out, "Note.")
        self.assertTrue(sum(stats.values()) >= 1)

    def test_fixture_mixed(self) -> None:
        text = FIXTURE.read_text(encoding="utf-8")
        out, stats = self.mod.strip_agent_comments(text)
        self.assertIn("@Ada Lee", out)
        self.assertNotIn("@Claude", out)
        self.assertNotIn("Claude (2026-07-21)", out)
        self.assertIn("Keep this human comment", out)
        self.assertIn("Bare after unwrap", out)
        self.assertGreaterEqual(sum(stats.values()), 2)


if __name__ == "__main__":
    unittest.main()
