#!/usr/bin/env python3
"""Tests for the manuscript-writing tracked-change tool (scripts/track_edit.py)."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "skills/manuscript-writing/scripts/track_edit.py"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ZOTERO_JSON = json.dumps({
    "citationID": "abc12345",
    "properties": {"formattedCitation": "(Boyd, 1993)", "plainCitation": "(Boyd, 1993)", "noteIndex": 0},
    "citationItems": [{"id": 1, "itemData": {"id": 1, "type": "article-journal", "author": [{"family": "Boyd"}]}}],
})


def run(text: str) -> str:
    return f'<w:r><w:t xml:space="preserve">{text}</w:t></w:r>'


def field(display: str, instr: str) -> str:
    return ('<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
            f'<w:r><w:instrText xml:space="preserve">{instr}</w:instrText></w:r>'
            '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
            f'{run(display)}'
            '<w:r><w:fldChar w:fldCharType="end"/></w:r>')


PARAGRAPHS = [
    run("Growth slowed as breeding densities at the first colonies reached saturation ")
    + field("(Boyd, 1993)", " ADDIN ZOTERO_ITEM CSL_CITATION " + ZOTERO_JSON.replace("&", "&amp;").replace("<", "&lt;") + " ")
    + run(", whereas the oldest colonies here had the lowest densities."),
    run("Pup counts were made from drone images."),
]


def make_docx(path: Path) -> None:
    body = "".join(f"<w:p>{p}</w:p>" for p in PARAGRAPHS)
    document = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                f'<w:document xmlns:w="{W}"><w:body>{body}<w:sectPr/></w:body></w:document>')
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("[Content_Types].xml",
                   '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                   '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                   '<Default Extension="xml" ContentType="application/xml"/>'
                   '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
        z.writestr("_rels/.rels",
                   '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
        z.writestr("word/", "")  # a folder entry, which the tool must drop
        z.writestr("word/document.xml", document)


class TestTrackEdit(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.src = self.dir / "in.docx"
        self.dst = self.dir / "out.docx"
        make_docx(self.src)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_tool(self, edits: list[dict], *extra: str, dst: Path | None = None) -> subprocess.CompletedProcess[str]:
        spec = self.dir / "edits.json"
        spec.write_text(json.dumps(edits), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(TOOL), str(self.src), str(dst or self.dst), "--edits", str(spec),
             "--author", "Test Author", "--date", "2026-01-01T00:00:00Z", *extra],
            capture_output=True, text=True)

    def output_xml(self) -> str:
        with zipfile.ZipFile(self.dst) as z:
            self.assertNotIn("word/", z.namelist())
            return z.read("word/document.xml").decode()

    def test_changes_only_the_edited_words_and_keeps_the_field(self) -> None:
        proc = self.run_tool([{
            "find": "first colonies reached saturation",
            "text": "Growth slowed as breeding densities at the first colonies became saturated (Boyd, 1993), "
                    "whereas the oldest colonies here had the lowest densities.",
        }])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        xml = self.output_xml()
        inserted = "".join(re.findall(r"<w:ins [^>]*>.*?</w:ins>", xml))
        deleted = "".join(re.findall(r"<w:del [^>]*>.*?</w:del>", xml))
        self.assertIn("became saturated", inserted)
        self.assertIn("reached saturation", deleted)
        self.assertNotIn("Growth slowed", inserted + deleted)  # unchanged words stay untracked
        self.assertIn("ZOTERO_ITEM", xml)
        self.assertNotIn("ZOTERO_ITEM", deleted)  # the live citation field survives
        self.assertIn('w:author="Test Author"', xml)

    def test_refuses_a_citation_that_would_become_plain_text(self) -> None:
        proc = self.run_tool([{
            "find": "first colonies reached saturation",
            "text": "Growth slowed as breeding densities reached saturation (Boyd, 1993; Lee, 2001), "
                    "whereas the oldest colonies here had the lowest densities.",
        }])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("(Boyd, 1993; Lee, 2001)", proc.stdout)
        self.assertFalse(self.dst.exists())

    def test_find_must_match_exactly_one_paragraph(self) -> None:
        proc = self.run_tool([{"find": "ro", "text": "x"}])
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("matched 2 paragraphs", proc.stdout + proc.stderr)

    def test_second_run_on_its_own_output_gets_new_revision_ids(self) -> None:
        first = self.run_tool([{"find": "drone", "text": "Pups were counted on drone images."}])
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        self.src, second_dst = self.dst, self.dir / "out2.docx"
        second = self.run_tool([{
            "find": "first colonies reached saturation",
            "text": "Growth slowed as breeding densities at the first colonies became saturated (Boyd, 1993), "
                    "whereas the oldest colonies here had the lowest densities.",
        }], dst=second_dst)
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        with zipfile.ZipFile(second_dst) as z:
            xml = z.read("word/document.xml").decode()
        ids = re.findall(r'<w:(?:ins|del) w:id="(\d+)"', xml)
        self.assertEqual(len(ids), len(set(ids)), ids)

    def test_refuses_to_overwrite_the_input(self) -> None:
        proc = self.run_tool([{"find": "drone", "text": "Pups were counted on drone images."}], dst=self.src)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("new file", proc.stdout + proc.stderr)

    def test_unchanged_field_stays_untracked_when_text_on_both_sides_changes(self) -> None:
        proc = self.run_tool([{
            "find": "first colonies reached saturation",
            "text": "Growth slowed at dense colonies (Boyd, 1993). Oldest sites had lower densities.",
        }])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        xml = self.output_xml()
        inserted = "".join(re.findall(r"<w:ins [^>]*>.*?</w:ins>", xml))
        deleted = "".join(re.findall(r"<w:del [^>]*>.*?</w:del>", xml))
        self.assertIn("ZOTERO_ITEM", xml)
        self.assertNotIn("ZOTERO_ITEM", deleted)
        self.assertNotIn("ZOTERO_ITEM", inserted)

    def test_accept_existing_accepts_revisions_and_demotes_empty_sectpr_heading(self) -> None:
        src = self.dir / "tracked.docx"
        body = (
            '<w:p><w:pPr><w:pStyle w:val="Heading1"/><w:sectPr/></w:pPr></w:p>'
            '<w:p><w:r><w:t xml:space="preserve">Pup </w:t></w:r>'
            '<w:del w:id="1" w:author="Old" w:date="2025-01-01T00:00:00Z"><w:r><w:delText>numbers</w:delText></w:r></w:del>'
            '<w:ins w:id="2" w:author="Old" w:date="2025-01-01T00:00:00Z"><w:r><w:t>counts</w:t></w:r></w:ins>'
            '<w:r><w:t xml:space="preserve"> were recorded.</w:t></w:r></w:p>'
        )
        document = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                    f'<w:document xmlns:w="{W}"><w:body>{body}<w:sectPr/></w:body></w:document>')
        with zipfile.ZipFile(src, "w") as z:
            z.writestr("[Content_Types].xml",
                       '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                       '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                       '<Default Extension="xml" ContentType="application/xml"/>'
                       '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
            z.writestr("_rels/.rels",
                       '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                       '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
            z.writestr("word/document.xml", document)
        self.src = src
        proc = self.run_tool([{"find": "Pup counts were recorded.", "text": "Pup counts were logged."}], "--accept-existing")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        xml = self.output_xml()
        self.assertNotIn('w:author="Old"', xml)
        self.assertNotIn('w:val="Heading1"', xml)
        self.assertIn("<w:sectPr/>", xml)
        self.assertIn("logged", xml)


if __name__ == "__main__":
    unittest.main()
