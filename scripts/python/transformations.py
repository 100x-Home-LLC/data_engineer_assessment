import json
from pathlib import Path
from typing import List, Dict
import pandas as pd
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine


# Load environment variables
load_dotenv(dotenv_path=r"C:\\Home_LLC_Vijay_bagal\\data_engineer_assessment\\.env.development")

# Database configuration from .env
db_config = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# Create SQLAlchemy engine
engine = create_engine(
    f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
INPUT_JSON: str = r"C:\\Home_LLC_Vijay_bagal\\data_engineer_assessment\\data\\fake_property_data.json"
FIELD_CONFIG_XLSX: str = r"C:/Home_LLC_Vijay_bagal/data_engineer_assessment/data/Field Config.xlsx"
NESTED_FIELDS: List[str] = ["Valuation", "HOA", "Rehab"]
PRIMARY_KEY_FIELD: str = "Property_ID"

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def explode_nested(records: List[Dict], field_name: str, pk_field: str) -> pd.DataFrame:
    exploded_rows: List[Dict] = []
    for rec in records:
        for item in rec.get(field_name, []):
            item[pk_field] = rec[pk_field]
            exploded_rows.append(item)
    return pd.DataFrame(exploded_rows)

# ---------------------------------------------------------------------------
# Main ETL pipeline
# ---------------------------------------------------------------------------
def main() -> None:
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data: List[Dict] = json.load(f)

    for idx, rec in enumerate(data, start=1):
        rec[PRIMARY_KEY_FIELD] = idx

    main_df: pd.DataFrame = pd.json_normalize(data, sep="_")

    cols_to_drop = [c for c in NESTED_FIELDS if c in main_df.columns]
    main_df.drop(columns=cols_to_drop, inplace=True)

    # Extract nested fields
    valuation_df = explode_nested(data, "Valuation", PRIMARY_KEY_FIELD)
    hoa_df_nested = explode_nested(data, "HOA", PRIMARY_KEY_FIELD)
    rehab_df = explode_nested(data, "Rehab", PRIMARY_KEY_FIELD)

    # Load field config from Excel
    field_config_raw = pd.read_excel(FIELD_CONFIG_XLSX)
    field_config_raw["Target Table"] = field_config_raw["Target Table"].str.lower()

    field_config: Dict[str, List[str]] = (
        field_config_raw.groupby("Target Table")["Column Name"]
        .apply(list)
        .to_dict()
    )

    # Ensure all fields from field config are preserved, even if same as table name
    property_df = main_df[[PRIMARY_KEY_FIELD] + [f for f in field_config.get("property", []) if f in main_df.columns]]
    leads_df = main_df[[PRIMARY_KEY_FIELD] + [f for f in field_config.get("leads", []) if f in main_df.columns]]
    hoa_df = hoa_df_nested[[PRIMARY_KEY_FIELD] + [f for f in field_config.get("hoa", []) if f in hoa_df_nested.columns]]

    
    return property_df, leads_df, hoa_df, valuation_df, rehab_df

if __name__ == "__main__":
    property_df, leads_df, hoa_df, valuation_df, rehab_df = main()


# # Write each DataFrame to its corresponding MySQL table
property_df.to_sql(name="property", con=engine, if_exists="append", index=False)
leads_df.to_sql(name="leads", con=engine, if_exists="append", index=False)
hoa_df.to_sql(name="hoa", con=engine, if_exists="append", index=False)
valuation_df.to_sql(name="valuation", con=engine, if_exists="append", index=False)
rehab_df.to_sql(name="rehab", con=engine, if_exists="append", index=False)




