from pathlib import Path
from collections import Counter
import json,sys
ROOT=Path(__file__).resolve().parent.parent

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def fail(message):
    print('ERROR:',message,file=sys.stderr);sys.exit(1)

d=load(ROOT/'site/data/master.json')
e=d.get('entries')
if not isinstance(e,list) or not e: fail('missing or empty entries')
try:
    version=tuple(int(x) for x in d['meta']['version'].lstrip('vV').split('.'))
except (KeyError,ValueError,AttributeError): fail('invalid version')
if version<(0,2,40):fail('master is older than 0.2.40')
ids=[x.get('id') for x in e]
if any(not isinstance(i,str) or not i.strip() for i in ids):fail('empty ID')
duplicates=[i for i,n in Counter(ids).items() if n>1]
if duplicates:fail('duplicate IDs: '+', '.join(duplicates[:10]))
if any(not x.get('name') for x in e):fail('empty name')
existing=set(ids); baseline=set(load(ROOT/'scripts/baseline-ids.json'))
missing=sorted(baseline-existing)
if missing:fail('baseline IDs missing: '+', '.join(missing[:10]))
broken=[(x['id'],i) for x in e for i in (x.get('links') or []) if i not in existing]
if broken:fail('unresolved forward links: '+str(broken[:10]))
for f in ['proposals.json','geo-notes.json','source-audit.json']:load(ROOT/'site/data'/f)
print('OK version',d['meta']['version'],'entities',len(e),'links',sum(len(x.get('links') or []) for x in e),'baseline IDs retained',len(baseline))
