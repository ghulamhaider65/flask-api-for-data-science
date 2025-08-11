"""Simple smoke tests for API endpoints using Flask test client."""
from io import BytesIO
import sys
import pathlib
import pandas as pd

# Ensure project root is on path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

from flask_data_insight_api.app import create_app  # noqa: E402

app = create_app()
client = app.test_client()

def print_section(title):
	print(f"\n=== {title} ===")

print_section('HEALTH')
resp = client.get('/health')
print('Status:', resp.status_code, 'JSON:', resp.json)

print_section('UPLOAD')
csv_bytes = b"a,b,c\n1,2,3\n4,5,6\n"
resp = client.post('/upload', data={'file': (BytesIO(csv_bytes), 'sample.csv')}, content_type='multipart/form-data')
print('Status:', resp.status_code)
print('Keys:', list(resp.json.keys()) if resp.is_json else None)

print_section('PREDICT')
df = pd.DataFrame({'f1':[1,2,3,4,5],'f2':[5,4,3,2,1],'target':[0,1,0,1,0]})
buf = BytesIO()
df.to_csv(buf, index=False)
buf.seek(0)
resp = client.post('/predict', data={'file': (buf, 'train.csv')}, content_type='multipart/form-data')
print('Status:', resp.status_code)
print('JSON:', resp.json if resp.is_json else None)
