from __future__ import annotations
from typing import Dict, Any
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


TARGET_COLUMN = 'target'

def train_simple_model(df: pd.DataFrame) -> Dict[str, Any]:
    if TARGET_COLUMN not in df.columns:
        return {'trained': False, 'reason': f"Column '{TARGET_COLUMN}' not found."}
    # Only keep numeric features for simplicity
    feature_df = df.drop(columns=[TARGET_COLUMN])
    feature_df = feature_df.select_dtypes(include='number')
    if feature_df.empty:
        return {'trained': False, 'reason': 'No numeric features available.'}
    X = feature_df
    y = df[TARGET_COLUMN]
    # If classification target is numeric but continuous, attempt binning (simple heuristic)
    if y.nunique() > 20 and y.dtype != 'object':
        y = pd.qcut(y, q=4, duplicates='drop')
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    except ValueError as e:
        return {'trained': False, 'reason': str(e)}

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    return {
        'trained': True,
        'model': 'RandomForestClassifier',
        'accuracy': float(acc),
        'n_features': int(X.shape[1]),
        'n_rows': int(df.shape[0])
    }
