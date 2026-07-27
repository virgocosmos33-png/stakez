import json, urllib.request
from pathlib import Path
HERE = Path('.')
jobs = json.loads(Path('put_jobs.json').read_text(encoding='utf-8'))
for job in jobs:
    path = HERE / job['file']
    data = path.read_bytes()
    req = urllib.request.Request(job['url'], data=data, method='PUT')
    with urllib.request.urlopen(req, timeout=120) as resp:
        print(job['file'], job['upload_id'], resp.status, len(data))
print('PUT_DONE')
