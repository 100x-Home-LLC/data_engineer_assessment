import pandas as pd
from typing import List

def drop_columns(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """Remove specified columns if they exist in the DataFrame."""
    return df.drop(columns=[col for col in cols if col in df.columns], errors='ignore')

def replace_null_like_values(df: pd.DataFrame) -> pd.DataFrame:
    """Replace various null-like string values with pd.NA across all columns."""
    null_patterns = {"", "null", "none", "nan", "na", "n/a","Null"}
    for col in df.columns:
        df[col] = df[col].astype(str).apply(
            lambda x: pd.NA if x.strip().lower() in null_patterns else x
        )
    return df

def clean_boolean_columns(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """Standardize boolean values (Yes/No, True/False, 1/0) to actual bool types."""
    bool_map = {
        'yes': True, 'no': False,
        'true': True, 'false': False,
        '1': True, '0': False
    }
    for col in cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower().map(bool_map).fillna(pd.NA)
    return df

def fill_missing_categoricals(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """Fill missing values in categorical columns with 'Unknown'."""
    for col in cols:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")
    return df




