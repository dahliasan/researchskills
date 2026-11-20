#!/usr/bin/env python3
"""Apply paragraph rewrites to a .docx as word-level tracked changes.

Usage:
    python track_edit.py IN.docx OUT.docx --edits edits.json --author "Name"

edits.json is a list of objects, one per paragraph:
    {"find": "text that occurs in exactly one paragraph", "text": "the whole new paragraph"}
or  {"para_id": "1A2B3C4D", "text": "..."}

`find` matches the paragraph's current text with all tracked changes accepted.
`text` is the full replacement paragraph in plain text. Wrap italics in
*asterisks*. Citation fields (Zotero or other) are kept when their displayed
text, for example "(Smith et al., 2020)", appears in `text`; an existing
Zotero citation can be reused anywhere by writing its displayed text.

The tool diffs word by word, so only changed words become insertions and
deletions. Existing revisions, comments, fields and formatting are kept.
Before writing, it checks that:
  * accepting all changes gives exactly the requested text, and
  * rejecting this run's changes gives back the input document unchanged.
If either check fails, nothing is written and the exit code is 1.
"""
from __future__ import annotations

import argparse
import copy
import json
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from lxml import etree

sys.path.insert(0, str(Path(__file__).resolve().parent))

from track_changes import engine  # noqa: E402
from track_changes.dlib import accepted_text, q  # noqa: E402
from track_changes.revtools import accept_all, canonical, read_xml, reject_ids, serialize, write_docx  # noqa: E402

PARAID = '{%s}paraId' % engine.W14
ZOTERO = 'ZOTERO_ITEM'
# A parenthetical that names a year, for example "(Smith et al., 2020)" or "(Boyd, 1993; Lee, 2001a)".
CITATION_RE = re.compile(r'\((?=[^()]*[A-Z][^()]*\b(?:1[6-9]|20)\d{2}[a-z]?\b)[^()]*\)')


def field_library(tree):
    """Displayed text -> field runs, for every field in the document."""
    lib, reusable = {}, set()
    for p in tree.getroot().iter(q('w:p')):
        for a in engine.atomize(p, strict=False):
            if a.kind != 'f':
                continue
            lib.setdefault(a.text, [copy.deepcopy(r) for r in a.runs])
            if ZOTERO in engine.field_instr(a.runs):
                reusable.add(a.text)
    return lib, reusable


def find_paragraph(tree, edit):
    pars = list(tree.getroot().iter(q('w:p')))
    if 'para_id' in edit:
        hits = [p for p in pars if p.get(PARAID) == edit['para_id']]
        key = f"para_id {edit['para_id']}"
    else:
        hits = [p for p in pars if edit['find'] in accepted_text(p)]
        key = f"find {edit['find'][:60]!r}"
    if len(hits) != 1:
        raise SystemExit(f'error: {key} matched {len(hits)} paragraphs; it must match exactly one')
    return hits[0]


def dedupe_citation_ids(tree, mine):
    """Give copied Zotero fields fresh citationIDs so Zotero treats them as separate citations."""
    seen = {}
    for p in tree.getroot().iter(q('w:p')):
        for a in engine.atomize(p, strict=False):
            if a.kind != 'f' or ZOTERO not in engine.field_instr(a.runs):
                continue
            js = engine.zotero_json(a.runs)
            is_mine = any(anc.tag == q('w:ins') and anc.get(q('w:id')) in mine
                          for anc in a.runs[0].iterancestors())
            seen.setdefault(js['citationID'], []).append((is_mine, a.runs, js))
    fixed = 0
    for group in seen.values():
        if len(group) < 2:
            continue
        keep_first_mine = all(m for m, _, _ in group)
        for k, (is_mine, runs, js) in enumerate(group):
            if not is_mine or (keep_first_mine and k == 0):
                continue
            js['citationID'] = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(8))
            instr = [e for r in runs for e in r.iter(q('w:instrText'))]
            instr[0].text = ' ADDIN ZOTERO_ITEM CSL_CITATION ' + json.dumps(js, ensure_ascii=False, separators=(',', ':')) + ' '
            engine.set_preserve(instr[0])
            for e in instr[1:]:
                e.getparent().remove(e)
            fixed += 1
    return fixed


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('src')
    ap.add_argument('dst')
    ap.add_argument('--edits', required=True, help='JSON file with the paragraph edits')
    ap.add_argument('--author', required=True, help='revision author shown in Word')
    ap.add_argument('--date', default=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
    ap.add_argument('--keep-italic', action='append', default=[],
                    help='term whose existing italics must not change (repeatable)')
    ap.add_argument('--allow-plain-citations', action='store_true',
                    help='allow citation-like text that matches no existing field')
    ap.add_argument('--seed', type=int, default=0)
    args = ap.parse_args(argv)

    if Path(args.src).resolve() == Path(args.dst).resolve():
        raise SystemExit('error: write to a new file; keep the input as the baseline')
    random.seed(args.seed)
    engine.AUTHOR, engine.DATE = args.author, args.date
    engine.KEEP_ITALIC[:] = args.keep_italic
    edits = json.loads(Path(args.edits).read_text(encoding='utf-8'))

    original = read_xml(args.src)
    tree = read_xml(args.src)
    lib, reusable = field_library(tree)
    plain_cites = []
    for edit in edits:
        for m in CITATION_RE.finditer(engine.parse_target(edit['text'])[0]):
            if m.group(0) not in lib:
                plain_cites.append(m.group(0))
    if plain_cites and not args.allow_plain_citations:
        print('error: these citations match no field in the document and would become plain text '
              '(Zotero would no longer manage them):')
        for c in plain_cites:
            print(f'  {c}')
        print('Use the exact displayed text of an existing field, insert the citation in Word with '
              'Zotero afterwards, or pass --allow-plain-citations.')
        return 1
    ids = engine.Ids()
    log, targets = [], []
    for n, edit in enumerate(edits):
        par = find_paragraph(tree, edit)
        plain = engine.edit_paragraph(par, edit['text'], lib, reusable, ids, log, name=str(n))
        targets.append((par, plain))
    fixed_ids = dedupe_citation_ids(tree, ids.mine)

    bad = 0
    for par, plain in targets:
        alone = accept_all(etree.ElementTree(copy.deepcopy(par))).getroot()
        got = accepted_text(alone)
        if got != plain:
            bad += 1
            print(f'ACCEPT MISMATCH\n  got: {got!r}\n  exp: {plain!r}')
    if canonical(reject_ids(copy.deepcopy(tree), ids.mine)) != canonical(original):
        bad += 1
        print('REJECT MISMATCH: rejecting this run does not restore the input')

    for name, changes, _, conflicts in log:
        print(f'paragraph {name}: {len(changes)} change(s)')
        for d, i in changes:
            print(f'  - {d!r}\n  + {i!r}')
        for c in conflicts:
            print(f'  formatting conflict skipped: {c!r}')
    print(f'citation IDs refreshed: {fixed_ids}')
    if bad:
        print(f'{bad} check(s) failed; nothing written')
        return 1
    write_docx(args.src, args.dst, {'word/document.xml': serialize(tree)})
    print(f'wrote {args.dst} ({len(ids.mine)} revisions by {args.author})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
