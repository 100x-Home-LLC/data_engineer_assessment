import pandas as pd
from extract import load_json_data, flatten_data, explode_nested
from transform import load_field_config, split_main_tables, clean_all_tables
from config import NESTED_FIELDS, PRIMARY_KEY_FIELD
from database import get_engine


def main():
    data = load_json_data()
    main_df = flatten_data(data, NESTED_FIELDS)

    valuation_df = explode_nested(data, "Valuation")
    hoa_df_raw = explode_nested(data, "HOA")
    rehab_df = explode_nested(data, "Rehab")

    field_config = load_field_config()
    main_tables = split_main_tables(main_df, field_config)

    property_df = main_tables.get("property", pd.DataFrame())
    leads_df = main_tables.get("leads", pd.DataFrame())
    hoa_df = hoa_df_raw[[PRIMARY_KEY_FIELD] + [f for f in field_config.get("hoa", []) if f in hoa_df_raw.columns]]

# Load into MySQL database
    engine = get_engine()
    property_df.to_sql(name="property", con=engine, if_exists="append", index=False)
    leads_df.to_sql(name="leads", con=engine, if_exists="append", index=False)
    hoa_df.to_sql(name="hoa", con=engine, if_exists="append", index=False)
    valuation_df.to_sql(name="valuation", con=engine, if_exists="append", index=False)
    rehab_df.to_sql(name="rehab", con=engine, if_exists="append", index=False)

    return clean_all_tables(property_df, leads_df, hoa_df, valuation_df, rehab_df)




if __name__ == "__main__":
    property_df, leads_df, hoa_df, valuation_df, rehab_df = main()