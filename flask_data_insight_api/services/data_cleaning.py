from __future__ import annotations
import pandas as pd
from typing import Tuple


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Basic cleaning: drop completely empty columns
    df = df.dropna(axis=1, how='all')
    # Fill numeric NaNs with median, categorical with mode
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            median = df[col].median()
            df[col] = df[col].fillna(median)
        else:
            if df[col].mode().empty:
                df[col] = df[col].fillna('unknown')
            else:
                mode = df[col].mode().iloc[0]
                df[col] = df[col].fillna(mode)
    return df
