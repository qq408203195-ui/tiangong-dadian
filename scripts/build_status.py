from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import json, os, subprocess

ROOT = Path(__file__).resolve().parent.parent
def load(p):
    return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))

db = load('site/data/master.json')
kernel = load('data/kernel.json')
source41 = load('data/v0.2.41-provenance.json')
recipes = load('data/v0.2.41-recipes.json')
entries = db['entries']
ids = {e['id'] for e in entries}
geo = [e['id'] for e in entries if e.get('category') == '地理志']
baseline = load('scripts/baseline-ids.json')
missing = sorted(set(baseline) - ids)
broken = [(e['id'], x) for e in entries for x in e.get('links', []) if x not in ids]
categories = Counter(e.get('category', '未分类') for e in entries)
recipe_missing_references = 0
recipe_missing_facilities = 0
for recipe in recipes:
    parts = list(recipe.get('inputs') or []) + [recipe.get('output') or {}, recipe.get('facility') or {}]
    if any(not part.get('resolved_id') or part['resolved_id'] not in ids for part in parts):
        recipe_missing_references += 1
    if (recipe.get('facility') or {}).get('resolved_id') not in ids:
        recipe_missing_facilities += 1
sha = os.environ.get('GITHUB_SHA') or subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
status = {
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'commit': sha,
    'run_url': f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{os.environ.get('GITHUB_REPOSITORY', 'qq408203195-ui/tiangong-dadian')}/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}",
    'test_status': 'passed' if os.environ.get('TIANGONG_TESTS_PASSED') == '1' else 'not_verified',
    'version': db['meta']['version'], 'required_minimum': '0.2.41',
    'baseline_is_old': tuple(map(int, db['meta']['version'].lstrip('vV').split('.'))) < (0, 2, 41),
    'entities': len(entries), 'geography': len(geo), 'baseline_ids_missing': len(missing),
    'broken_forward_links': len(broken), 'categories': dict(categories),
    'registered_core_objects': len(kernel['objects']),
    'registered_facts': len(kernel['facts']), 'registered_conflicts': len(kernel['conflicts']),
    'available_html': source41,
    'recipe_reference_audit': {'total': len(recipes), 'incomplete': recipe_missing_references, 'missing_facility': recipe_missing_facilities},
    'fact_checks_in_legacy_data': sum(len(e.get('fact_checks') or []) for e in entries),
    'historical_snapshot': {'source': '原对话对 V0.2.41 的审计描述，尚未重新读取', 'entities': 2476, 'geography': 1556, 'version': '0.2.41'},
}
out = ROOT / 'site/progress/status.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Wrote', out)
