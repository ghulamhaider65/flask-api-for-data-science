from __future__ import annotations
import os
from pathlib import Path
from typing import Dict, Any
from werkzeug.utils import secure_filename
from flask import current_app
import pandas as pd


def save_uploaded_file(file_storage) -> Path:
    filename = secure_filename(file_storage.filename)
    if not filename:
        raise ValueError('Empty filename.')
    ext = Path(filename).suffix.lower()
    if ext not in current_app.config['UPLOAD_EXTENSIONS']:
        raise ValueError(f'Unsupported file extension: {ext}')
    dest = Path(current_app.config['DATA_DIR']) / filename
    file_storage.save(dest)
    return dest


def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def basic_insights(df: pd.DataFrame) -> Dict[str, Any]:
    null_counts = df.isna().sum().to_dict()
    dtypes = {k: str(v) for k, v in df.dtypes.items()}
    return {
        'rows': int(df.shape[0]),
        'columns': int(df.shape[1]),
        'null_counts': null_counts,
        'dtypes': dtypes,
    }
