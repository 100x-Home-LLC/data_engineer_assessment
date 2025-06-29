import json
import pandas as pd
from typing import List, Dict
from config import INPUT_JSON, PRIMARY_KEY_FIELD


def load_json_data() -> List[Dict]:
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    for idx, rec in enumerate(data, start=1):
        rec[PRIMARY_KEY_FIELD] = idx
    return data


def flatten_data(data: List[Dict], nested_fields: List[str]) -> pd.DataFrame:
    df = pd.json_normalize(data, sep="_")
    df.drop(columns=[c for c in nested_fields if c in df.columns], inplace=True)
    return df


def explode_nested(data: List[Dict], field: str) -> pd.DataFrame:
    rows = []
    for rec in data:
        for item in rec.get(field, []):
            item[PRIMARY_KEY_FIELD] = rec[PRIMARY_KEY_FIELD]
            rows.append(item)
    return pd.DataFrame(rows)