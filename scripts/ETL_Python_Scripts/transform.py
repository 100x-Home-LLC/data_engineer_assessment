import pandas as pd
from typing import Dict, List
from config import FIELD_CONFIG_XLSX, PRIMARY_KEY_FIELD
from cleaner import (
    drop_columns,
    replace_null_like_values,
    clean_boolean_columns,
    fill_missing_categoricals,
)


def load_field_config() -> Dict[str, List[str]]:
    """Load and return field configuration from Excel file as a dictionary."""
    config_df = pd.read_excel(FIELD_CONFIG_XLSX)
    config_df["Target Table"] = config_df["Target Table"].str.lower()
    return config_df.groupby("Target Table")["Column Name"].apply(list).to_dict()


def split_main_tables(df: pd.DataFrame, config: Dict[str, List[str]]) -> Dict[str, pd.DataFrame]:
    """Split the flattened DataFrame into individual tables based on the config."""
    return {
        table: df[[PRIMARY_KEY_FIELD] + [f for f in fields if f in df.columns]]
        for table, fields in config.items()
    }


def clean_all_tables(property_df, leads_df, hoa_df, valuation_df, rehab_df):
    

    # Property table
    property_df = drop_columns(property_df, ['Unnamed: 0', 'Property_Title'])
    property_df = replace_null_like_values(property_df)
    property_df = clean_boolean_columns(property_df, ['Flood', 'Train', 'Pool', 'BasementYesNo'])
    property_df = fill_missing_categoricals(property_df, ['Flood', 'Train', 'Pool', 'BasementYesNo'])

    # Leads table
    leads_df = drop_columns(leads_df, ['Unnamed: 0'])
    leads_df = replace_null_like_values(leads_df)
    leads_df = fill_missing_categoricals(leads_df, ['Reviewed_Status', 'Most_Recent_Status', 'Source', 'Seller_Retained_Broker'])

    # HOA table
    hoa_df = drop_columns(hoa_df, ['Unnamed: 0'])
    hoa_df = replace_null_like_values(hoa_df)
    hoa_df = clean_boolean_columns(hoa_df, ['HOA_Flag'])
    hoa_df = fill_missing_categoricals(hoa_df, ['HOA_Flag'])

    # Rehab table
    rehab_df = drop_columns(rehab_df, ['Unnamed: 0'])
    rehab_df = replace_null_like_values(rehab_df)
    rehab_bool_cols = [col for col in rehab_df.columns if any(x in col.lower() for x in ['flag', 'paint', 'roof'])]
    rehab_df = clean_boolean_columns(rehab_df, rehab_bool_cols)
    rehab_df = fill_missing_categoricals(rehab_df, rehab_bool_cols)

    # Valuation table
    valuation_df = drop_columns(valuation_df, ['Unnamed: 0'])
    valuation_df = replace_null_like_values(valuation_df)

    return property_df, leads_df, hoa_df, valuation_df, rehab_df
