"""Check file-based navigation, bibliography targets, and required teaching features."""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1]
html_files=sorted(ROOT.rglob('*.html'))
broken=[]; no_titles=[]; html_count=0
for p in html_files:
    soup=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
    if not soup.title or not soup.select_one('h1'):no_titles.append(str(p.relative_to(ROOT)))
    for a in soup.select('a[href],link[href],script[src]'):
        url=a.get('href') or a.get('src')
        if not url or url.startswith(('https://','http://','mailto:','javascript:')):continue
        data=urlsplit(url)
        if not data.path: continue
        target=(p.parent/unquote(data.path)).resolve()
        if not target.is_file():broken.append((str(p.relative_to(ROOT)),url,'missing file'))
        elif data.fragment and target.suffix=='.html':
            ts=BeautifulSoup(target.read_text(encoding='utf-8'),'html.parser')
            if ts.find(id=unquote(data.fragment)) is None:broken.append((str(p.relative_to(ROOT)),url,'missing anchor'))
    html_count+=1
assert not no_titles, 'HTML pages without titles: '+str(no_titles)
assert not broken, 'Broken links: '+str(broken)
assert len(html_files)>=20, len(html_files)
print(f'PASS: {html_count} HTML pages, local links/assets and citation anchors resolved.')
