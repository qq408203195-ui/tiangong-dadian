from html.parser import HTMLParser
from pathlib import Path
import hashlib, json

root = Path(__file__).resolve().parent.parent
def read(path):
    return json.loads((root/path).read_text(encoding='utf-8-sig'))
class Scripts(HTMLParser):
    def __init__(self):
        super().__init__(); self.current=None; self.parts={}
    def handle_starttag(self, tag, attrs):
        ident=dict(attrs).get('id')
        if tag=='script' and ident in ('db','m007','recipes'):
            self.current=ident; self.parts[ident]=[]
    def handle_data(self, data):
        if self.current: self.parts[self.current].append(data)
    def handle_endtag(self, tag):
        if tag=='script': self.current=None
source=root/'sources/天工大典_V0.2.41_离线百科.html'
provenance=read('data/v0.2.41-provenance.json')
assert hashlib.sha256(source.read_bytes()).hexdigest()==provenance['sha256']
parser=Scripts(); parser.feed(source.read_text(encoding='utf-8-sig'))
embedded={k:json.loads(''.join(v)) for k,v in parser.parts.items()}
ids=[e['id'] for e in embedded['db']]
assert len(ids)==2476 and len(set(ids))==2476
assert set(read('scripts/baseline-ids.json'))==set(ids)
assert {e['id'] for e in embedded['db'] if e.get('category')=='地理志'}==set(read('scripts/baseline-geography-ids.json'))
for k in ('m007','recipes'):
    assert embedded[k]==read('data/v0.2.41-'+k+'.json')
print('V0.2.41 HTML snapshot, embedded IDs and candidate exports verified')
