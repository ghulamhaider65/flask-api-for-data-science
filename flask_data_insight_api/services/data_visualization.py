from __future__ import annotations
from pathlib import Path
from typing import List
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-GUI backend for server environments
import matplotlib.pyplot as plt
import seaborn as sns


def generate_histograms(df: pd.DataFrame, plots_dir: Path, max_plots: int = 5) -> List[str]:
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    saved = []
    for col in numeric_cols[:max_plots]:
        plt.figure(figsize=(4,3))
        sns.histplot(df[col], kde=False, bins=20)
        plt.title(f'Histogram - {col}')
        fname = f'hist_{col}.png'
        out = plots_dir / fname
        plt.tight_layout()
        plt.savefig(out)
        plt.close()
        saved.append(fname)
    return saved


def generate_correlation_heatmap(df: pd.DataFrame, plots_dir: Path) -> str | None:
    numeric_df = df.select_dtypes(include='number')
    if numeric_df.shape[1] < 2:
        return None
    corr = numeric_df.corr(numeric_only=True)
    plt.figure(figsize=(6,5))
    sns.heatmap(corr, annot=False, cmap='viridis')
    plt.title('Correlation Heatmap')
    fname = 'correlation_heatmap.png'
    out = plots_dir / fname
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    return fname
