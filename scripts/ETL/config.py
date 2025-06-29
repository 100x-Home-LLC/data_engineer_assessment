import os
from dotenv import load_dotenv

# load_dotenv(".env.development")
load_dotenv(dotenv_path=r"data_engineer_assessment/.env.development")

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

INPUT_JSON = r"data_engineer_assessment/data/fake_property_data.json"
FIELD_CONFIG_XLSX = r"data_engineer_assessment/data/Field Config.xlsx"
PRIMARY_KEY_FIELD = "Property_ID"
NESTED_FIELDS = ["Valuation", "HOA", "Rehab"]