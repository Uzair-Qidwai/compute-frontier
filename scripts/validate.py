"""Standard-library checks for the portable static project."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path

root = Path(__file__).resolve().parents[1]
dist = root / 'dist'
class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.paths = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for key in ('src', 'href'):
            value = attrs.get(key, '')
            if value.startswith('./'):
                self.paths.append(value[2:].split('#')[0])
page = Page()
page.feed((dist / 'index.html').read_text())
assert len(page.ids) == len(set(page.ids)), 'Duplicate HTML IDs'
for path in page.paths:
    assert (dist / path).is_file(), f'Missing asset: {path}'
rows = json.loads((dist / 'data.json').read_text())
assert len({r['id'] for r in rows}) == len(rows), 'Duplicate record IDs'
for r in rows:
    assert r['capacity'] is None or r['capacity'] >= 0
    assert -129 <= r['lon'] <= -62 and 14 <= r['lat'] <= 58
context = json.loads((dist / 'market-context.json').read_text())
assert all(v['gw'] > 0 for v in context['country']['values'])
assert [v['year'] for v in context['forecast']['values']] == [2027, 2028, 2029]
assert [v['gw'] for v in context['forecast']['values']] == [88, 100, 112]
for p in dist.iterdir():
    if p.suffix in {'.html', '.css', '.js', '.json', '.csv', '.md'}:
        assert not re.search(r'cb1_[A-Za-z0-9_]+|ghp_[A-Za-z0-9]+|github_pat_[A-Za-z0-9_]+', p.read_text()), f'Possible credential in {p.name}'
print(f'PASS: {len(rows)} records, unique IDs, coordinate bounds, local assets, forecast values and credential-pattern scan.')
