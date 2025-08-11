import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'
PLOTS_DIR = BASE_DIR / 'static' / 'plots'
UPLOAD_EXTENSIONS = {'.csv'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    MAX_CONTENT_LENGTH = MAX_CONTENT_LENGTH
    DATA_DIR = DATA_DIR
    PLOTS_DIR = PLOTS_DIR
    UPLOAD_EXTENSIONS = UPLOAD_EXTENSIONS

# Ensure directories exist at import time
for d in (DATA_DIR, PLOTS_DIR):
    d.mkdir(parents=True, exist_ok=True)
