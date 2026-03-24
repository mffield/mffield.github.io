#!/usr/bin/env python3
"""Generate Academic Pages content from the archived Hugo site.

Usage:
    python generate_from_old_hugo.py /path/to/oldsite /path/to/output_bundle
"""

import os
import re
import sys
import html
import glob
import yaml
import shutil
import unicodedata
from pathlib import Path

def slugify(s: str) -> str:
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return re.sub(r'-+', '-', s)

def yaml_single_quote(s: str) -> str:
    return "'" + str(s).replace("'", "''") + "'"

def normalize_title(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode('ascii')
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

def doi_to_url(doi):
    if not doi:
        return None
    doi = str(doi).strip()
    if doi.startswith('http://') or doi.startswith('https://'):
        return doi
    return f'https://doi.org/{doi}'

def strip_md_italics(s):
    if s is None:
        return ''
    return re.sub(r'^\*+|\*+$', '', str(s).strip())

def parse_bib_entries(bib_text):
    entries = []
    i = 0
    n = len(bib_text)
    while True:
        at = bib_text.find('@', i)
        if at == -1:
            break
        m = re.match(r'@(\w+)\s*[{(]', bib_text[at:], re.S)
        if not m:
            i = at + 1
            continue
        brace_pos = at + m.end() - 1
        open_ch = bib_text[brace_pos]
        close_ch = '}' if open_ch == '{' else ')'
        depth = 0
        j = brace_pos
        while j < n:
            ch = bib_text[j]
            if ch == open_ch:
                depth += 1
            elif ch == close_ch:
                depth -= 1
                if depth == 0:
                    break
            j += 1
        entries.append(bib_text[at:j+1])
        i = j + 1
    return entries

def parse_bib_entry(block):
    m = re.match(r'@(\w+)\s*[{(]\s*([^,]+)\s*,', block, re.S)
    if not m:
        return None
    etype = m.group(1).lower()
    key = m.group(2).strip()
    body = block[m.end():-1].strip()
    fields = {}
    i = 0
    while i < len(body):
        while i < len(body) and body[i] in ' \t\r\n,':
            i += 1
        if i >= len(body):
            break
        m2 = re.match(r'([A-Za-z_][A-Za-z0-9_\-]*)\s*=\s*', body[i:])
        if not m2:
            break
        fname = m2.group(1).lower()
        i += m2.end()
        if body[i] == '{':
            depth = 0
            startv = i + 1
            while i < len(body):
                ch = body[i]
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        val = body[startv:i]
                        i += 1
                        break
                i += 1
        elif body[i] == '"':
            i += 1
            startv = i
            while i < len(body):
                ch = body[i]
                if ch == '"' and body[i-1] != '\\':
                    val = body[startv:i]
                    i += 1
                    break
                i += 1
        else:
            startv = i
            while i < len(body) and body[i] not in ',\r\n':
                i += 1
            val = body[startv:i].strip()
        fields[fname] = re.sub(r'\s+', ' ', val.strip())
        while i < len(body) and body[i] not in ',':
            i += 1
        if i < len(body) and body[i] == ',':
            i += 1
    return {'entrytype': etype, 'key': key, **fields}

def main(old_root: Path, out_root: Path):
    if out_root.exists():
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True)

    pubs_dir = out_root / '_publications'
    bib_dir = out_root / 'files' / 'bib'
    pubs_dir.mkdir(parents=True, exist_ok=True)
    bib_dir.mkdir(parents=True, exist_ok=True)

    bib_text = (old_root / 'publications.bib').read_text(encoding='utf-8')
    blocks = parse_bib_entries(bib_text)
    bib_entries = [parse_bib_entry(b) for b in blocks]
    bib_by_title = {normalize_title(b.get('title')): b for b in bib_entries if b}

    for p in sorted((old_root / 'content/publication').glob('*/index.md')):
        if p.parent.name == 'preprint':
            continue
        txt = p.read_text(encoding='utf-8')
        _, fm_txt, body = txt.split('---', 2)
        fm = yaml.safe_load(fm_txt) or {}

        title = str(fm.get('title')).strip()
        date = str(fm.get('date')).strip()
        venue = strip_md_italics(fm.get('publication'))
        authors = fm.get('authors') or []
        tags = fm.get('tags') or []
        doi = fm.get('doi')
        doi_url = doi_to_url(doi)
        pub_type = (fm.get('publication_types') or [''])[0]
        category = 'conferences' if 'conference' in pub_type else 'manuscripts'
        pub_slug = slugify(title)

        bib = bib_by_title.get(normalize_title(title))
        citation = f"{', '.join(authors)}. ({date[:4]}). &quot;{html.escape(title)}.&quot; <i>{html.escape(venue)}</i>."

        bibtexurl = None
        if bib:
            block = next((b for b in blocks if re.match(rf'@\w+\s*[{{(]]\s*{re.escape(bib['key'])}\s*,', b, re.S)), None)
            if block:
                bib_name = f"{pub_slug}.bib"
                (bib_dir / bib_name).write_text(block.strip() + '\n', encoding='utf-8')
                bibtexurl = f"/files/bib/{bib_name}"

        lines = [
            '---',
            f'title: {yaml_single_quote(title)}',
            'collection: publications',
            f'category: {category}',
            f'permalink: /publication/{date}-{pub_slug}',
            f'excerpt: {yaml_single_quote(venue or title)}',
            f'date: {date}',
            f'venue: {yaml_single_quote(venue)}',
        ]
        if doi_url:
            lines.append(f'paperurl: {yaml_single_quote(doi_url)}')
        if bibtexurl:
            lines.append(f'bibtexurl: {yaml_single_quote(bibtexurl)}')
        lines.append(f'citation: {yaml_single_quote(citation)}')
        lines.append('---')
        lines.append('')
        lines.append(f"**Authors:** {', '.join(authors)}")
        if doi_url:
            lines.extend(['', f"**DOI:** [{doi}]({doi_url})"])
        if tags:
            lines.extend(['', f"**Keywords:** {', '.join(tags)}"])

        (pubs_dir / f"{date}-{pub_slug}.md").write_text('\n'.join(lines) + '\n', encoding='utf-8')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(__doc__)
        raise SystemExit(1)
    main(Path(sys.argv[1]), Path(sys.argv[2]))
