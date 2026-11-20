"""Accept-all, reject-mine and canonical comparison for OOXML documents."""
import copy
import zipfile

from lxml import etree

from .dlib import W, q

CHANGE_TAGS = ['rPrChange', 'pPrChange', 'sectPrChange', 'tblPrChange', 'tblGridChange',
               'tcPrChange', 'trPrChange', 'numberingChange']
KEEP_IN_DEL = {q('w:commentRangeStart'), q('w:commentRangeEnd'), q('w:bookmarkStart'), q('w:bookmarkEnd')}


def is_mark(e):
    p = e.getparent()
    return p is not None and p.tag in (q('w:rPr'), q('w:trPr'))


def accept_all(tree, stats=None):
    root = tree.getroot()
    st = stats if stats is not None else {}
    # table rows
    for tr in list(root.iter(q('w:tr'))):
        trpr = tr.find(q('w:trPr'))
        if trpr is None:
            continue
        if trpr.find(q('w:del')) is not None:
            n = len(list(tr.iter(q('w:commentRangeStart'))))
            st['rows_deleted'] = st.get('rows_deleted', 0) + 1
            st['comments_in_deleted_rows'] = st.get('comments_in_deleted_rows', 0) + n
            tr.getparent().remove(tr)
        else:
            for m in trpr.findall(q('w:ins')):
                trpr.remove(m)
    # run-level deletions
    for d in list(root.iter(q('w:del'))):
        if is_mark(d) or d.getparent() is None:
            continue
        parent = d.getparent()
        keep = []
        for e in d.iter():
            if e.tag in KEEP_IN_DEL:
                keep.append(e)
            elif e.tag == q('w:r') and e.find(q('w:commentReference')) is not None:
                keep.append(e)
        for e in keep:
            if e.tag == q('w:r'):
                for k in list(e):
                    if k.tag not in (q('w:rPr'), q('w:commentReference')):
                        e.remove(k)
            d.addprevious(e)
        parent.remove(d)
    # insertions
    for i in list(root.iter(q('w:ins'))):
        if i.getparent() is None:
            continue
        if is_mark(i):
            i.getparent().remove(i)
            continue
        parent = i.getparent()
        idx = list(parent).index(i)
        for k in list(i):
            parent.insert(idx, k)
            idx += 1
        parent.remove(i)
    for t in CHANGE_TAGS:
        for e in list(root.iter(q('w:' + t))):
            e.getparent().remove(e)
    # deleted paragraph marks: merge with following paragraph
    marks = [m for m in root.iter(q('w:del')) if is_mark(m)]
    pars = []
    for m in marks:
        p = m.getparent().getparent().getparent()
        assert p.tag == q('w:p'), p.tag
        pars.append((p, m))
    for p, m in reversed(pars):
        m.getparent().remove(m)
        nxt = p.getnext()
        if nxt is None or nxt.tag != q('w:p'):
            st['mark_del_unmerged'] = st.get('mark_del_unmerged', 0) + 1
            continue
        if p.find(q('w:pPr') + '/' + q('w:sectPr')) is not None:
            st['mark_del_sectpr'] = st.get('mark_del_sectpr', 0) + 1
        nppr = nxt.find(q('w:pPr'))
        idx = 0 if nppr is None else list(nxt).index(nppr) + 1
        for k in [k for k in p if k.tag != q('w:pPr')]:
            nxt.insert(idx, k)
            idx += 1
        p.getparent().remove(p)
        st['merged'] = st.get('merged', 0) + 1
    return tree


def reject_ids(tree, ids):
    root = tree.getroot()
    for i in list(root.iter(q('w:ins'))):
        if i.get(q('w:id')) not in ids or i.getparent() is None:
            continue
        if is_mark(i):
            p = i.getparent().getparent().getparent()
            p.getparent().remove(p)
        else:
            i.getparent().remove(i)
    for c in list(root.iter(q('w:rPrChange'))):
        if c.get(q('w:id')) not in ids:
            continue
        rpr = c.getparent()
        inner = c.find(q('w:rPr'))
        for k in list(rpr):
            rpr.remove(k)
        for k in (list(inner) if inner is not None else []):
            rpr.append(k)
        if len(rpr) == 0:
            rpr.getparent().remove(rpr)
    for d in list(root.iter(q('w:del'))):
        if d.get(q('w:id')) not in ids or d.getparent() is None:
            continue
        if is_mark(d):
            rpr = d.getparent()
            rpr.remove(d)
            continue
        for e in d.iter(q('w:delText'), q('w:delInstrText')):
            e.tag = q('w:t') if e.tag == q('w:delText') else q('w:instrText')
        parent = d.getparent()
        idx = list(parent).index(d)
        for k in list(d):
            parent.insert(idx, k)
            idx += 1
        parent.remove(d)
    return tree


def _strip_attrs(e):
    c = copy.deepcopy(e)
    for x in c.iter():
        for a in list(x.attrib):
            if 'rsid' in a or a.endswith('}paraId') or a.endswith('}textId'):
                del x.attrib[a]
    return etree.tostring(c, method='c14n')


def canonical(tree):
    """Sequence describing text, formatting, revision context, fields and comment anchors."""
    out = []
    body = tree.getroot().find(q('w:body'))

    def ctx(el):
        c = []
        p = el.getparent()
        while p is not None and p.tag not in (q('w:p'), q('w:body')):
            if p.tag in (q('w:ins'), q('w:del')):
                c.append((etree.QName(p).localname, p.get(q('w:author')), p.get(q('w:date'))))
            elif p.tag == q('w:hyperlink'):
                c.append(('hl', tuple(sorted(p.attrib.items()))))
            p = p.getparent()
        return tuple(c)

    rpr_cache = {}
    for e in body.iter():
        tag = e.tag
        if not isinstance(tag, str):
            continue
        ln = etree.QName(tag).localname
        if ln in ('t', 'delText', 'instrText', 'delInstrText'):
            r = e.getparent()
            rpr = r.find(q('w:rPr'))
            sig = b'' if rpr is None or len(rpr) == 0 else _strip_attrs(rpr)
            cx = ctx(r)
            for ch in e.text or '':
                out.append((ln, ch, sig, cx))
        elif ln in ('tab', 'br', 'cr', 'drawing', 'sym', 'fldChar'):
            if ln == 'drawing' or e.getparent().tag == q('w:r'):
                out.append((ln, tuple(sorted((k, v) for k, v in e.attrib.items())), ctx(e.getparent())))
        elif ln in ('commentRangeStart', 'commentRangeEnd', 'commentReference', 'bookmarkStart', 'bookmarkEnd'):
            out.append((ln, e.get(q('w:id')), e.get(q('w:name'))))
        elif ln == 'p':
            ppr = e.find(q('w:pPr'))
            if ppr is not None:
                ppr = copy.deepcopy(ppr)
                for r in ppr.findall(q('w:rPr')):
                    if len(r) == 0:
                        ppr.remove(r)
            out.append(('P', _strip_attrs(ppr) if ppr is not None and len(ppr) else b''))
        elif ln in ('tblPr', 'trPr', 'tcPr', 'tblGrid', 'sectPr'):
            if e.getparent().tag != q('w:pPr'):
                out.append((ln, _strip_attrs(e)))
    return out


def read_xml(docx, name='word/document.xml'):
    with zipfile.ZipFile(docx) as z:
        data = z.read(name)
    return etree.ElementTree(etree.fromstring(data, etree.XMLParser(huge_tree=True)))


def write_docx(src_docx, dst_docx, replacements):
    """Copy src to dst replacing parts {name: bytes}."""
    with zipfile.ZipFile(src_docx) as zi, zipfile.ZipFile(dst_docx, 'w', zipfile.ZIP_DEFLATED) as zo:
        for info in zi.infolist():
            if info.is_dir():
                continue  # folder entries break cloud sync and co-editing
            data = replacements.get(info.filename, None)
            if data is None:
                data = zi.read(info.filename)
            zo.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED)


def serialize(tree):
    return etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
