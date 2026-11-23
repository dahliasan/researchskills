"""Link in-text figure and table references to their captions with Word cross-reference fields.

Bookmarks each caption's SEQ field (adding SEQ Supplementary_Figure to plain-text
"Supplementary Fig. N." captions), then replaces each in-text number after
Fig./Figure/Table(s)/Supplementary Fig./Supplementary Table with a REF field
(\\h hyperlink) showing the same number. Visible text is unchanged.

Usage: python link_xrefs.py IN.docx OUT.docx

Refuses to write unless the plain text (accepted, rejected and all markup, via
pandoc) is identical before and after. The field swaps are not tracked: the
visible text does not change.
"""
import copy
import random
import re
import sys
from lxml import etree

import os
import shutil
import subprocess
import tempfile
import zipfile

src_docx, out_docx = sys.argv[1], sys.argv[2]
d = tempfile.mkdtemp()
with zipfile.ZipFile(src_docx) as z:
    z.extractall(d)
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
q = lambda t: "{%s}%s" % (W, t)
XS = "{http://www.w3.org/XML/1998/namespace}space"
path = f"{d}/word/document.xml"
tree = etree.parse(path)
root = tree.getroot()

bm_ids = [int(b.get(q("id"))) for b in root.iter(q("bookmarkStart")) if b.get(q("id"), "").isdigit()]
next_bm = [max(bm_ids or [0]) + 1]
used_names = {b.get(q("name")) for b in root.iter(q("bookmarkStart"))}


def new_bookmark():
    while True:
        name = "_Ref%09d" % random.randint(100000000, 999999999)
        if name not in used_names:
            used_names.add(name)
            break
    s = etree.Element(q("bookmarkStart")); s.set(q("id"), str(next_bm[0])); s.set(q("name"), name)
    e = etree.Element(q("bookmarkEnd")); e.set(q("id"), str(next_bm[0]))
    next_bm[0] += 1
    return name, s, e


def deleted(el):
    return any(a.tag == q("del") for a in el.iterancestors())


def field_runs(rpr, instr, result):
    out = []
    for kind in ("begin", "instr", "separate", "result", "end"):
        r = etree.Element(q("r"))
        if rpr is not None:
            r.append(copy.deepcopy(rpr))
        if kind == "instr":
            t = etree.SubElement(r, q("instrText")); t.text = instr; t.set(XS, "preserve")
        elif kind == "result":
            t = etree.SubElement(r, q("t")); t.text = result
        else:
            etree.SubElement(r, q("fldChar")).set(q("fldCharType"), kind)
        out.append(r)
    return out


def text_run(rpr, text):
    r = etree.Element(q("r"))
    if rpr is not None:
        r.append(copy.deepcopy(rpr))
    t = etree.SubElement(r, q("t")); t.text = text; t.set(XS, "preserve")
    return r


def plain_runs(p):
    """(run, t) for live text runs outside any field, in order."""
    out, depth, in_result = [], 0, []
    for r in p.iter(q("r")):
        if deleted(r):
            continue
        fc = r.find(q("fldChar"))
        if fc is not None:
            typ = fc.get(q("fldCharType"))
            if typ == "begin":
                depth += 1; in_result.append(False)
            elif typ == "separate" and in_result:
                in_result[-1] = True
            elif typ == "end" and in_result:
                depth -= 1; in_result.pop()
            continue
        t = r.find(q("t"))
        if t is not None and depth == 0:
            out.append((r, t))
    return out


def replace_span(run, t, start, end, new_runs):
    """Split run around t.text[start:end] and put new_runs in the middle."""
    if len([c for c in run if c.tag != q("rPr")]) != 1:
        raise ValueError("run has several children")
    rpr = run.find(q("rPr"))
    text = t.text
    seq = []
    if text[:start]:
        seq.append(text_run(rpr, text[:start]))
    seq += new_runs
    if text[end:]:
        seq.append(text_run(rpr, text[end:]))
    for x in seq:
        run.addprevious(x)
    run.getparent().remove(run)


targets = {}  # (seq name, number) -> bookmark name

# 1. Bookmark existing SEQ caption fields
for p in root.iter(q("p")):
    runs = [r for r in p.iter(q("r")) if not deleted(r)]
    i = 0
    while i < len(runs):
        fc = runs[i].find(q("fldChar"))
        if fc is not None and fc.get(q("fldCharType")) == "begin":
            j, instr, result, sep, depth = i, "", "", False, 0
            while j < len(runs):
                f = runs[j].find(q("fldChar"))
                if f is not None:
                    typ = f.get(q("fldCharType"))
                    depth += typ == "begin"; depth -= typ == "end"
                    if typ == "separate" and depth == 1:
                        sep = True
                it = runs[j].find(q("instrText"))
                if it is not None:
                    instr += it.text or ""
                t = runs[j].find(q("t"))
                if sep and t is not None:
                    result += t.text or ""
                if depth == 0:
                    break
                j += 1
            m = re.match(r"\s*SEQ\s+(\w+)", instr)
            if m:
                key = (m.group(1), result.strip())
                assert key not in targets, key
                prev = runs[i].getprevious()
                if prev is not None and prev.tag == q("bookmarkStart") and prev.get(q("name"), "").startswith("_Ref"):
                    targets[key] = prev.get(q("name"))  # already bookmarked by an earlier run
                else:
                    name, s, e = new_bookmark()
                    runs[i].addprevious(s); runs[j].addnext(e)
                    targets[key] = name
            i = j + 1
        else:
            i += 1

# 2. Plain-text "Supplementary Fig. N." captions -> SEQ Supplementary_Figure
for p in root.iter(q("p")):
    st = p.find(q("pPr") + "/" + q("pStyle"))
    if st is None or st.get(q("val")) != "Caption":
        continue
    pr = plain_runs(p)
    if not pr:
        continue
    r0, t0 = pr[0]
    m = re.match(r"(Supplementary Fig\. )(\d+)(\.)", t0.text or "")
    if not m:
        continue
    num = m.group(2)
    name, s, e = new_bookmark()
    fr = field_runs(r0.find(q("rPr")), " SEQ Supplementary_Figure \\* ARABIC ", num)
    replace_span(r0, t0, m.start(2), m.end(2), [s, *fr, e])
    targets[("Supplementary_Figure", num)] = name

# 3. In-text references -> REF fields
label_seq = [
    (r"Supplementary Fig\.\s*", "Supplementary_Figure"),
    (r"Supplementary Table\s*", "Supplementary_Table"),
    (r"(?<!Supplementary )(?:Fig\.|Figure)\s*", "Figure"),
    (r"(?<!Supplementary )Tables?\s*", "Table"),
]
pat = re.compile("|".join("(?P<g%d>%s)(?P<n%d>\\d+)(?:(?P<a%d>\\s+and\\s+)(?P<m%d>\\d+))?" % (i, lab, i, i, i)
                          for i, (lab, _) in enumerate(label_seq)))
done, skipped = 0, []
for p in list(root.iter(q("p"))):
    pr = plain_runs(p)
    s = "".join(t.text for _, t in pr)
    hits = []
    for m in pat.finditer(s):
        gi = next(i for i in range(len(label_seq)) if m.group("n%d" % i))
        seqname = label_seq[gi][1]
        # skip the caption's own label ("Figure 1." at a caption start already holds a SEQ field)
        for grp in ("n%d" % gi, "m%d" % gi):
            if m.group(grp):
                hits.append((m.start(grp), m.end(grp), seqname, m.group(grp)))
    # map string offsets to (run, t); apply right-to-left within each t
    pos, spans = 0, []
    for r, t in pr:
        spans.append((pos, pos + len(t.text), r, t)); pos += len(t.text)
    for a, b, seqname, num in sorted(hits, reverse=True):
        key = (seqname, num)
        if key not in targets:
            skipped.append((key, s[max(0, a - 30):b + 5])); continue
        host = [x for x in spans if x[0] <= a and b <= x[1]]
        if not host:
            skipped.append((key, "spans runs")); continue
        lo, hi, r, t = host[0]
        fr = field_runs(r.find(q("rPr")), " REF %s \\h " % targets[key], num)
        replace_span(r, t, a - lo, b - lo, fr)
        # later hits in the same t were already handled (right-to-left); refresh spans for earlier ones
        pr = plain_runs(p)
        pos, spans = 0, []
        for r2, t2 in pr:
            spans.append((pos, pos + len(t2.text), r2, t2)); pos += len(t2.text)
        done += 1

tree.write(path, xml_declaration=True, encoding="UTF-8", standalone=True)
print("bookmarked captions:", sorted(targets))
print("REF fields inserted:", done)
for k in skipped:
    print("SKIPPED", k)

with zipfile.ZipFile(src_docx) as zi, zipfile.ZipFile(out_docx, "w", zipfile.ZIP_DEFLATED) as zo:
    for it in zi.infolist():
        zo.write(os.path.join(d, it.filename), it.filename)
shutil.rmtree(d)


def plain(f, mode):
    return subprocess.run(["pandoc", f, "-t", "plain", "--track-changes=" + mode],
                          capture_output=True, text=True, check=True).stdout


for mode in ("accept", "reject", "all"):
    if plain(src_docx, mode) != plain(out_docx, mode):
        os.remove(out_docx)
        sys.exit(f"text changed in {mode} view; nothing written")
print("text identical in accepted, rejected and all-markup views; wrote", out_docx)
