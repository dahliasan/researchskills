"""Word-level tracked-change engine for OOXML paragraphs (lxml)."""
import copy
import difflib
import json
import random
import re
import string

from lxml import etree

from .dlib import W, q, in_deleted

AUTHOR = 'Author'
DATE = '2000-01-01T00:00:00Z'
W14 = 'http://schemas.microsoft.com/office/word/2010/wordml'
XML_SPACE = '{http://www.w3.org/XML/1998/namespace}space'

VISIBLE = {q('w:t'), q('w:tab'), q('w:br'), q('w:cr'), q('w:drawing'), q('w:sym'),
           q('w:noBreakHyphen'), q('w:object'), q('w:pict')}
WRAPPABLE = VISIBLE | {q('w:fldChar'), q('w:instrText')}
XCHAR = {q('w:tab'): '\t', q('w:br'): '\n', q('w:cr'): '\n', q('w:noBreakHyphen'): '‑',
         q('w:sym'): '?', q('w:drawing'): '￼', q('w:object'): '￼', q('w:pict'): '￼'}

RPR_ORDER = ['rStyle', 'rFonts', 'b', 'bCs', 'i', 'iCs', 'caps', 'smallCaps', 'strike', 'dstrike',
             'outline', 'shadow', 'emboss', 'imprint', 'noProof', 'snapToGrid', 'vanish', 'webHidden',
             'color', 'spacing', 'w', 'kern', 'position', 'sz', 'szCs', 'highlight', 'u', 'effect',
             'bdr', 'shd', 'fitText', 'vertAlign', 'rtl', 'cs', 'em', 'lang', 'eastAsianLayout',
             'specVanish', 'oMath']


class Ids:
    def __init__(self, start=20000, split_start=40000):
        self.n = start
        self.s = split_start
        self.mine = set()
        self.splitmap = {}

    def next(self):
        self.n += 1
        self.mine.add(str(self.n))
        return str(self.n)

    def split(self):
        self.s += 1
        return str(self.s)


def rev(tag, ids):
    e = etree.Element(q(tag))
    e.set(q('w:id'), ids.next())
    e.set(q('w:author'), AUTHOR)
    e.set(q('w:date'), DATE)
    return e


# ---------------------------------------------------------------- atoms
class Atom:
    __slots__ = ('kind', 'text', 'run', 'child', 'off', 'runs')

    def __init__(self, kind, text, run=None, child=None, off=0, runs=None):
        self.kind, self.text, self.run, self.child, self.off, self.runs = kind, text, run, child, off, runs

    def __repr__(self):
        return f'Atom({self.kind},{self.text!r})'


def atomize(par, strict=True):
    atoms = []
    stack = []  # field state per level: 'instr' / 'result'
    cur = None  # current top-level field atom
    for r in par.iter(q('w:r')):
        if in_deleted(r, par):
            continue
        if cur is not None and r not in cur.runs:
            cur.runs.append(r)
        for c in r:
            tag = c.tag
            if tag == q('w:fldChar'):
                ft = c.get(q('w:fldCharType'))
                if ft == 'begin':
                    if not stack:
                        cur = Atom('f', '', runs=[r])
                    stack.append('instr')
                elif ft == 'separate':
                    if stack:
                        stack[-1] = 'result'
                elif ft == 'end':
                    if not stack:
                        assert not strict, 'field end without begin'
                        continue
                    stack.pop()
                    if not stack:
                        atoms.append(cur)
                        cur = None
            elif stack:
                if tag == q('w:t') and all(s == 'result' for s in stack):
                    cur.text += c.text or ''
            elif tag == q('w:t'):
                for k, ch in enumerate(c.text or ''):
                    atoms.append(Atom('c', ch, r, c, k))
            elif tag in XCHAR:
                atoms.append(Atom('x', XCHAR[tag], r, c, 0))
    assert not (stack and strict), 'unterminated field'
    return atoms


TOKEN_RE = re.compile(r'\w+|\s+|[^\w\s]')


def tokenize_atoms(atoms):
    """Return list of (key, a_start, a_end)."""
    toks = []
    i = 0
    n = len(atoms)
    while i < n:
        if atoms[i].kind == 'f':
            toks.append((('F', atoms[i].text), i, i + 1))
            i += 1
            continue
        j = i
        while j < n and atoms[j].kind != 'f':
            j += 1
        s = ''.join(a.text for a in atoms[i:j])
        for m in TOKEN_RE.finditer(s):
            toks.append((('T', m.group(0)), i + m.start(), i + m.end()))
        i = j
    return toks


# ---------------------------------------------------------------- target parsing
SUBS = {'₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9'}


def parse_target(md):
    """Return (plain, flags) where flags[i] = dict(i=bool, va=None|'subscript'|'superscript')."""
    assert md.count('*') % 2 == 0, md
    plain, flags = [], []
    ital = False
    for ch in md:
        if ch == '*':
            ital = not ital
            continue
        va = None
        if ch in SUBS:
            ch, va = SUBS[ch], 'subscript'
        plain.append(ch)
        flags.append({'i': ital, 'va': va})
    s = ''.join(plain)
    for m in re.finditer(r'(?<=m s)-1|(?<=mm d)-1', s):
        for k in range(m.start(), m.end()):
            flags[k]['va'] = 'superscript'
    return s, flags


def tokenize_target(plain, flags, field_counts, unlimited):
    """field_counts: Counter of displays allowed (limited); unlimited: set of displays."""
    toks = []
    counts = dict(field_counts)
    cands = sorted(set(counts) | set(unlimited), key=len, reverse=True)
    i, n = 0, len(plain)
    buf_start = 0

    def flush(a, b):
        for m in TOKEN_RE.finditer(plain[a:b]):
            toks.append((('T', m.group(0)), a + m.start(), a + m.end()))

    while i < n:
        hit = None
        if i == 0 or not (plain[i - 1].isalnum() and plain[i].isalnum()):
            for d in cands:
                if d and plain.startswith(d, i) and (counts.get(d, 0) > 0 or d in unlimited):
                    e = i + len(d)
                    if e == n or not (plain[e - 1].isalnum() and plain[e].isalnum()):
                        hit = d
                        break
        if hit:
            flush(buf_start, i)
            toks.append((('F', hit), i, i + len(hit)))
            if counts.get(hit, 0) > 0:
                counts[hit] -= 1
            i += len(hit)
            buf_start = i
        else:
            i += 1
    flush(buf_start, n)
    return toks


# ---------------------------------------------------------------- diff
def diff_ops(skeys, tkeys, stext_len, ttext_len):
    sm = difflib.SequenceMatcher(None, skeys, tkeys, autojunk=False)
    ops = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        t = 'eq' if tag == 'equal' else 'chg'
        if ops and ops[-1][0] == 'chg' and t == 'chg':
            o = ops[-1]
            ops[-1] = ('chg', o[1], i2, o[3], j2)
        else:
            ops.append((t, i1, i2, j1, j2))

    def has_field(i1, i2):
        return any(k[0] == 'F' for k in skeys[i1:i2])

    changed = True
    while changed:
        changed = False
        for k in range(1, len(ops) - 1):
            t, i1, i2, j1, j2 = ops[k]
            if t != 'eq' or ops[k - 1][0] != 'chg' or ops[k + 1][0] != 'chg':
                continue
            if has_field(i1, i2):
                continue
            L = stext_len(i1, i2)
            b, a = ops[k - 1], ops[k + 1]
            mb = max(stext_len(b[1], b[2]), ttext_len(b[3], b[4]))
            ma = max(stext_len(a[1], a[2]), ttext_len(a[3], a[4]))
            if L <= mb and L <= ma:
                ops[k - 1:k + 2] = [('chg', b[1], a[2], b[3], a[4])]
                changed = True
                break
    return ops


# ---------------------------------------------------------------- run surgery
def content_kids(run):
    return [k for k in run if k.tag != q('w:rPr')]


def set_preserve(t):
    t.set(XML_SPACE, 'preserve')


def split_before(run, child, off):
    """Split run so that a run begins at (child, off). Returns that run or None if at end."""
    kids = content_kids(run)
    idx = kids.index(child)
    if child.tag == q('w:t'):
        text = child.text or ''
        if off >= len(text):
            rest = kids[idx + 1:]
        elif off == 0:
            rest = kids[idx:]
        else:
            nt = etree.Element(q('w:t'))
            nt.text = text[off:]
            set_preserve(nt)
            child.text = text[:off]
            set_preserve(child)
            rest = [nt] + kids[idx + 1:]
    else:
        rest = kids[idx:] if off == 0 else kids[idx + 1:]
    if not rest:
        return None
    if rest[0] is kids[0]:
        return run
    nr = etree.Element(run.tag, attrib=dict(run.attrib))
    rpr = run.find(q('w:rPr'))
    if rpr is not None:
        nr.append(copy.deepcopy(rpr))
    for k in rest:
        nr.append(k)
    run.addnext(nr)
    return nr


def runs_between(par, start, end):
    out, on = [], False
    for r in par.iter(q('w:r')):
        if r is start:
            on = True
        if on:
            out.append(r)
        if r is end:
            break
    return out


def to_del_text(run):
    for el in run.iter(q('w:t'), q('w:instrText')):
        el.tag = q('w:delText') if el.tag == q('w:t') else q('w:delInstrText')


def wrap_del(runs, par, ids):
    made = set()
    for r in runs:
        if in_deleted(r, par):
            continue
        if not any(k.tag in WRAPPABLE for k in content_kids(r)):
            continue
        prev = r.getprevious()
        if prev is not None and prev in made:
            prev.append(r)
        else:
            d = rev('w:del', ids)
            r.addprevious(d)
            d.append(r)
            made.add(d)
        to_del_text(r)


def delete_atoms(par, atoms, a, b, ids):
    """Delete atoms[a..b] inclusive."""
    A, B = atoms[a], atoms[b]
    if B.kind == 'f':
        end_run = B.runs[-1]
    else:
        split_before(B.run, B.child, B.off + 1)
        end_run = B.run
    if A.kind == 'f':
        start_run = A.runs[0]
    else:
        start_run = split_before(A.run, A.child, A.off)
        if A.run is end_run:
            end_run = start_run
    wrap_del(runs_between(par, start_run, end_run), par, ids)


def climb_after(node, par, ids):
    while node.getparent() is not par:
        parent = node.getparent()
        if node.getnext() is None:
            node = parent
            continue
        nw = etree.Element(parent.tag, attrib=dict(parent.attrib))
        if parent.get(q('w:id')) is not None:
            sid = ids.split()
            ids.splitmap[sid] = ids.splitmap.get(parent.get(q('w:id')), parent.get(q('w:id')))
            nw.set(q('w:id'), sid)
        sib = node.getnext()
        while sib is not None:
            nxt = sib.getnext()
            nw.append(sib)
            sib = nxt
        parent.addnext(nw)
        node = parent
    return node


def climb_before(node, par, ids):
    while node.getparent() is not par:
        parent = node.getparent()
        if node.getprevious() is None:
            node = parent
            continue
        nw = etree.Element(parent.tag, attrib=dict(parent.attrib))
        if parent.get(q('w:id')) is not None:
            sid = ids.split()
            ids.splitmap[sid] = ids.splitmap.get(parent.get(q('w:id')), parent.get(q('w:id')))
            nw.set(q('w:id'), sid)
        sib = node
        while sib is not None:
            nxt = sib.getnext()
            nw.append(sib)
            sib = nxt
        parent.addnext(nw)
        node = nw
    return node


def clean_rpr(rpr):
    r = copy.deepcopy(rpr) if rpr is not None else etree.Element(q('w:rPr'))
    for tag in ('i', 'iCs', 'vertAlign', 'rPrChange', 'rStyle', 'highlight', 'u', 'b', 'bCs', 'ins', 'del'):
        for e in r.findall(q('w:' + tag)):
            r.remove(e)
    return r


def rpr_with(base, italic, va):
    r = copy.deepcopy(base)
    adds = []
    if italic:
        adds += [etree.Element(q('w:i')), etree.Element(q('w:iCs'))]
    if va:
        v = etree.Element(q('w:vertAlign'))
        v.set(q('w:val'), va)
        adds.append(v)
    kids = list(r) + adds
    for k in list(r):
        r.remove(k)
    kids.sort(key=lambda e: RPR_ORDER.index(etree.QName(e).localname)
              if etree.QName(e).localname in RPR_ORDER else 99)
    for k in kids:
        r.append(k)
    return r


def make_text_runs(chars_flags, base_rpr):
    """chars_flags: list of (ch, flags). Returns list of w:r."""
    runs = []
    cur_key, buf = None, []

    def emit():
        if not buf:
            return
        r = etree.Element(q('w:r'))
        rp = rpr_with(base_rpr, cur_key[0], cur_key[1])
        if len(rp):
            r.append(rp)
        t = etree.SubElement(r, q('w:t'))
        t.text = ''.join(buf)
        set_preserve(t)
        runs.append(r)

    for ch, f in chars_flags:
        key = (f['i'], f['va'])
        if key != cur_key:
            emit()
            cur_key, buf = key, []
        buf.append(ch)
    emit()
    return runs


def strip_field_copy(runs):
    out = []
    for r in runs:
        c = copy.deepcopy(r)
        for e in c.iter(q('w:delText'), q('w:delInstrText')):
            e.tag = q('w:t') if e.tag == q('w:delText') else q('w:instrText')
        for e in list(c.iter(q('w:rPrChange'))):
            e.getparent().remove(e)
        rpr = c.find(q('w:rPr'))
        if rpr is not None and len(rpr) == 0:
            c.remove(rpr)
        out.append(c)
    return out


def base_rpr_near(atoms, idx):
    """rPr of nearest plain char atom (outside fields) around idx."""
    order = list(range(idx, -1, -1)) + list(range(idx + 1, len(atoms)))
    for k in order:
        if 0 <= k < len(atoms) and atoms[k].kind == 'c':
            return clean_rpr(atoms[k].run.find(q('w:rPr')))
    return clean_rpr(None)


def build_insert(tgt_tokens, j1, j2, flags, plain, field_lib, base_rpr, ids):
    ins = rev('w:ins', ids)
    pending = []
    for k in range(j1, j2):
        key, a, b = tgt_tokens[k]
        if key[0] == 'F':
            for r in make_text_runs(pending, base_rpr):
                ins.append(r)
            pending = []
            for r in strip_field_copy(field_lib[key[1]]):
                ins.append(r)
        else:
            pending += [(plain[x], flags[x]) for x in range(a, b)]
    for r in make_text_runs(pending, base_rpr):
        ins.append(r)
    return ins


def insert_after_atom(par, atoms, idx, node_ins, ids):
    A = atoms[idx]
    if A.kind == 'f':
        head = A.runs[-1]
    else:
        split_before(A.run, A.child, A.off + 1)
        head = A.run
    node = climb_after(head, par, ids)
    node.addnext(node_ins)


def insert_before_atom(par, atoms, idx, node_ins, ids):
    A = atoms[idx]
    if A.kind == 'f':
        tail = A.runs[0]
    else:
        tail = split_before(A.run, A.child, A.off)
    node = climb_before(tail, par, ids)
    node.addprevious(node_ins)


def append_to_par(par, node_ins):
    par.append(node_ins)



KEEP_ITALIC = []  # terms whose existing italics the edit must not change; set by the caller


def run_fmt(run):
    rpr = run.find(q('w:rPr'))
    if rpr is None:
        return False, None
    i = rpr.find(q('w:i'))
    it = i is not None and i.get(q('w:val')) not in ('0', 'false')
    v = rpr.find(q('w:vertAlign'))
    va = v.get(q('w:val')) if v is not None else None
    if va == 'baseline':
        va = None
    return it, va


def format_atoms(par, atoms, a, b, italic, va, ids, log_conf):
    A, B = atoms[a], atoms[b]
    split_before(B.run, B.child, B.off + 1)
    end_run = B.run
    start_run = split_before(A.run, A.child, A.off)
    if A.run is end_run:
        end_run = start_run
    for r in runs_between(par, start_run, end_run):
        if in_deleted(r, par) or r.find(q('w:t')) is None:
            continue
        rpr = r.find(q('w:rPr'))
        if rpr is None:
            rpr = etree.Element(q('w:rPr'))
            r.insert(0, rpr)
        if rpr.find(q('w:rPrChange')) is not None:
            log_conf.append(''.join(t.text or '' for t in r.findall(q('w:t'))))
            continue
        old = [copy.deepcopy(k) for k in rpr]
        for tag in ('i', 'iCs', 'vertAlign'):
            for e in rpr.findall(q('w:' + tag)):
                rpr.remove(e)
        newr = rpr_with(rpr, italic, va)
        for k in list(rpr):
            rpr.remove(k)
        for k in newr:
            rpr.append(k)
        ch = rev('w:rPrChange', ids)
        inner = etree.SubElement(ch, q('w:rPr'))
        for k in old:
            inner.append(k)
        rpr.append(ch)

# ---------------------------------------------------------------- paragraph edit
def edit_paragraph(par, target_md, field_lib, unlimited, ids, log=None, name=''):
    atoms = atomize(par)
    stoks = tokenize_atoms(atoms)
    plain, flags = parse_target(target_md)
    fcount = {}
    for a in atoms:
        if a.kind == 'f':
            fcount[a.text] = fcount.get(a.text, 0) + 1
    ttoks = tokenize_target(plain, flags, fcount, unlimited)
    skeys = [t[0] for t in stoks]
    tkeys = [t[0] for t in ttoks]

    def slen(i1, i2):
        return sum(len(k[1]) for k in skeys[i1:i2])

    def tlen(j1, j2):
        return sum(len(k[1]) for k in tkeys[j1:j2])

    ops = diff_ops(skeys, tkeys, slen, tlen)
    conflicts = []
    # formatting (italic / vertAlign) of unchanged chars versus spec markup
    exempt = set()
    for w in KEEP_ITALIC:
        for m in re.finditer(re.escape(w), plain):
            exempt.update(range(m.start(), m.end()))
    mism = []
    fixes = {}  # op index -> list of (a_start, a_end_incl, italic, va)
    for oi, (t, i1, i2, j1, j2) in enumerate(ops):
        if t != 'eq':
            continue
        cur = None
        lst = []
        for (sk, sa, sb), (tk, ta, tb) in zip(stoks[i1:i2], ttoks[j1:j2]):
            for x in range(sb - sa):
                at = atoms[sa + x] if sk[0] != 'F' else None
                want = None
                if at is not None and at.kind == 'c' and not plain[ta + x].isspace() and (ta + x) not in exempt:
                    hi, hv = run_fmt(at.run)
                    wi, wv = flags[ta + x]['i'], flags[ta + x]['va']
                    if (hi, hv) != (wi, wv):
                        want = (wi, wv)
                        mism.append((plain[ta + x], (hi, hv), (wi, wv)))
                if want is not None and cur is not None and cur[3] == want and cur[1] == sa + x - 1:
                    cur[1] = sa + x
                elif want is not None:
                    if cur is not None:
                        lst.append(cur)
                    cur = [sa + x, sa + x, None, want]
                else:
                    if cur is not None:
                        lst.append(cur)
                    cur = None
        if cur is not None:
            lst.append(cur)
        if lst:
            fixes[oi] = lst
    changes = []
    for oi in range(len(ops) - 1, -1, -1):
        t, i1, i2, j1, j2 = ops[oi]
        if t == 'eq':
            for a0, a1, _, want in reversed(fixes.get(oi, [])):
                format_atoms(par, atoms, a0, a1, want[0], want[1], ids, log_conf=conflicts)
            continue
        del_txt = ''.join(k[1] for k in skeys[i1:i2])
        ins_txt = ''.join(k[1] for k in tkeys[j1:j2])
        changes.append((del_txt, ins_txt))
        if j2 > j1:
            anchor_idx = stoks[i2 - 1][2] - 1 if i2 > 0 else 0
            base = base_rpr_near(atoms, anchor_idx)
            node = build_insert(ttoks, j1, j2, flags, plain, field_lib, base, ids)
            if i2 > 0:
                insert_after_atom(par, atoms, stoks[i2 - 1][2] - 1, node, ids)
            elif atoms:
                insert_before_atom(par, atoms, 0, node, ids)
            else:
                append_to_par(par, node)
        if i2 > i1:
            delete_atoms(par, atoms, stoks[i1][1], stoks[i2 - 1][2] - 1, ids)
    if log is not None:
        log.append((name, list(reversed(changes)), mism, conflicts))
    return plain


def delete_paragraph(par, ids):
    atoms = atomize(par)
    if atoms:
        delete_atoms(par, atoms, 0, len(atoms) - 1, ids)
    mark_par(par, 'w:del', ids)


def mark_par(par, tag, ids):
    ppr = par.find(q('w:pPr'))
    if ppr is None:
        ppr = etree.Element(q('w:pPr'))
        par.insert(0, ppr)
    rpr = ppr.find(q('w:rPr'))
    if rpr is None:
        rpr = etree.Element(q('w:rPr'))
        # rPr precedes sectPr / pPrChange
        anchor = None
        for t in ('sectPr', 'pPrChange'):
            anchor = ppr.find(q('w:' + t))
            if anchor is not None:
                break
        if anchor is not None:
            anchor.addprevious(rpr)
        else:
            ppr.append(rpr)
    m = rev(tag, ids)
    pos = 0
    if tag == 'w:del' and rpr.find(q('w:ins')) is not None:
        pos = list(rpr).index(rpr.find(q('w:ins'))) + 1
    rpr.insert(pos, m)


def new_paragraph(template_par, target_md, base_rpr, ids):
    p = etree.Element(q('w:p'))
    p.set('{%s}paraId' % W14, '%08X' % random.randint(0x10000000, 0x7FFFFFFF))
    p.set('{%s}textId' % W14, '77777777')
    tppr = template_par.find(q('w:pPr'))
    if tppr is not None:
        ppr = copy.deepcopy(tppr)
        for e in list(ppr.iter(q('w:pPrChange'))):
            e.getparent().remove(e)
        rpr = ppr.find(q('w:rPr'))
        if rpr is not None:
            for e in list(rpr):
                if e.tag in (q('w:ins'), q('w:del'), q('w:rPrChange')):
                    rpr.remove(e)
            if len(rpr) == 0:
                ppr.remove(rpr)
        p.append(ppr)
    mark_par(p, 'w:ins', ids)
    plain, flags = parse_target(target_md)
    ins = rev('w:ins', ids)
    for r in make_text_runs(list(zip(plain, flags)), base_rpr):
        ins.append(r)
    p.append(ins)
    return p, plain


# ---------------------------------------------------------------- zotero synthesis
def field_instr(runs):
    s = ''.join((e.text or '') for r in runs for e in r.iter(q('w:instrText'), q('w:delInstrText')))
    return s


def zotero_json(runs):
    s = field_instr(runs).strip()
    pre = 'ADDIN ZOTERO_ITEM CSL_CITATION'
    assert s.startswith(pre), s[:60]
    return json.loads(s[len(pre):].strip())


def rtf_escape(s):
    return ''.join(c if ord(c) < 128 else '\\uc0\\u%d{}' % ord(c) for c in s)


def make_zotero_field(template_runs, items, plain):
    data = {
        'citationID': ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8)),
        'properties': {'formattedCitation': rtf_escape(plain), 'plainCitation': plain, 'noteIndex': 0},
        'citationItems': items,
        'schema': 'https://github.com/citation-style-language/schema/raw/master/csl-citation.json',
    }
    instr = ' ADDIN ZOTERO_ITEM CSL_CITATION ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ' '
    tr = strip_field_copy(template_runs)
    begin = next(r for r in tr if r.find(q('w:fldChar')) is not None and
                 r.find(q('w:fldChar')).get(q('w:fldCharType')) == 'begin')
    sep = next(r for r in tr if r.find(q('w:fldChar')) is not None and
               r.find(q('w:fldChar')).get(q('w:fldCharType')) == 'separate')
    end = next(r for r in tr if r.find(q('w:fldChar')) is not None and
               r.find(q('w:fldChar')).get(q('w:fldCharType')) == 'end')
    irun = next(r for r in tr if r.find(q('w:instrText')) is not None)
    for e in irun.findall(q('w:instrText'))[1:]:
        irun.remove(e)
    it = irun.find(q('w:instrText'))
    it.text = instr
    set_preserve(it)
    res = [r for r in tr if r.find(q('w:t')) is not None]
    rrun = res[0]
    for e in rrun.findall(q('w:t'))[1:]:
        rrun.remove(e)
    rrun.find(q('w:t')).text = plain
    return [begin, irun, sep, rrun, end]
