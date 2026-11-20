"""Helpers for reading OOXML paragraphs in accepted view."""
from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}


def q(tag):
    p, t = tag.split(':')
    return '{%s}%s' % (W, t)


def load(path):
    parser = etree.XMLParser(remove_blank_text=False, huge_tree=True)
    return etree.parse(path, parser)


def body_children(tree):
    body = tree.getroot().find(q('w:body'))
    return [c for c in body if isinstance(c.tag, str)]


def in_deleted(el, stop):
    """True if el is inside a w:del (or w:moveFrom) below stop."""
    p = el.getparent()
    while p is not None and p is not stop:
        if p.tag in (q('w:del'), q('w:moveFrom')):
            return True
        p = p.getparent()
    return False


def runs_in_order(par):
    """All w:r elements in document order inside paragraph (incl. nested in ins/del/hyperlink)."""
    return [r for r in par.iter(q('w:r'))]


def accepted_text(par, with_fields=True, mark_fields=False):
    """Visible text after accepting all changes. Field instructions excluded; field results included."""
    out = []
    depth = 0  # field nesting
    state = []  # per field: 'instr' or 'result'
    for r in runs_in_order(par):
        if in_deleted(r, par):
            continue
        for c in r:
            if c.tag == q('w:fldChar'):
                t = c.get(q('w:fldCharType'))
                if t == 'begin':
                    state.append('instr')
                    if mark_fields:
                        out.append('⟦')
                elif t == 'separate':
                    if state:
                        state[-1] = 'result'
                elif t == 'end':
                    if state:
                        state.pop()
                    if mark_fields:
                        out.append('⟧')
            elif c.tag == q('w:t'):
                if state and state[-1] == 'instr':
                    continue
                out.append(c.text or '')
            elif c.tag == q('w:tab'):
                out.append('\t')
            elif c.tag in (q('w:br'), q('w:cr')):
                out.append('\n')
            elif c.tag == q('w:noBreakHyphen'):
                out.append('‑')
            elif c.tag == q('w:sym'):
                out.append('?')
    return ''.join(out)


def style_of(par):
    ps = par.find(q('w:pPr') + '/' + q('w:pStyle'))
    return ps.get(q('w:val')) if ps is not None else ''
