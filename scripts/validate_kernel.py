from pathlib import Path
import json, sys
root = Path(__file__).resolve().parent.parent
data = json.loads((root/'data/kernel.json').read_text(encoding='utf-8'))
master = json.loads((root/'site/data/master.json').read_text(encoding='utf-8-sig'))
master_ids = {e['id'] for e in master['entries']}
assert data['schema_version'] == 1
for k in ('objects', 'facts', 'conflicts'):
    assert isinstance(data[k], list), k
seen = set()
for obj in data['objects']:
    assert isinstance(obj.get('id'), str) and obj['id'] in master_ids and obj['id'] not in seen
    assert obj.get('kind') in ('resource', 'building', 'recipe', 'technology', 'policy', 'unit', 'event', 'person', 'geography')
    assert obj.get('status') in ('candidate', 'tested')
    seen.add(obj['id'])
for fact in data['facts']:
    assert fact.get('entity_id') in master_ids and fact.get('claim')
    assert fact.get('status') in ('pending', 'disputed', 'verified')
    if fact['status'] == 'verified':
        sources = fact.get('sources', [])
        assert len({s.get('independent_group') for s in sources if s.get('independent_group') and s.get('locator') and s.get('url')}) >= 2, 'verified facts need two documented independent source groups'
print('Kernel structural checks passed; source independence still requires human review.')
