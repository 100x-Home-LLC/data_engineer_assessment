# Data Engineering Assessment

Welcome!  
This exercise evaluates your core **data-engineering** skills:

| Competency | Focus                                                         |
| ---------- | ------------------------------------------------------------- |
| SQL        | relational modelling, normalisation, DDL/DML scripting        |
| Python ETL | data ingestion, cleaning, transformation, & loading (ELT/ETL) |

---

## 0 Prerequisites & Setup

> **Allowed technologies**

- **Python ≥ 3.8** – all ETL / data-processing code
- **MySQL 8** – the target relational database
- **Lightweight helper libraries only** (e.g. `pandas`, `mysql-connector-python`).  
  List every dependency in **`requirements.txt`** and justify anything unusual.
- **No ORMs / auto-migration tools** – write plain SQL by hand.

---

## 1 Clone the skeleton repo

```
git clone https://github.com/100x-Home-LLC/data_engineer_assessment.git
```

✏️ Note: Rename the repo after cloning and add your full name.

**Start the MySQL database in Docker:**

```
docker-compose -f docker-compose.initial.yml up --build -d
```

- Database is available on `localhost:3306`
- Credentials/configuration are in the Docker Compose file
- **Do not change** database name or credentials

For MySQL Docker image reference:
[MySQL Docker Hub](https://hub.docker.com/_/mysql)

---

### Problem

- You are provided with a raw JSON file containing property records is located in data/
- Each row relates to a property. Each row mixes many unrelated attributes (property details, HOA data, rehab estimates, valuations, etc.).
- There are multiple Columns related to this property.
- The database is not normalized and lacks relational structure.
- Use the supplied Field Config.xlsx (in data/) to understand business semantics.

### Task

- **Normalize the data:**

  - Develop a Python ETL script to read, clean, transform, and load data into your normalized MySQL tables.
  - Refer the field config document for the relation of business logic
  - Use primary keys and foreign keys to properly capture relationships

- **Deliverable:**
  - Write necessary python and sql scripts
  - Place your scripts in `sql/` and `scripts/`
  - The scripts should take the initial json to your final, normalized schema when executed
  - Clearly document how to run your script, dependencies, and how it integrates with your database.

**Tech Stack:**

- Python (include a `requirements.txt`)
  Use **MySQL** and SQL for all database work
- You may use any CLI or GUI for development, but the final changes must be submitted as python/ SQL scripts
- **Do not** use ORM migrations—write all SQL by hand

---

## Submission Guidelines

- Edit the section to the bottom of this README with your solutions and instructions for each section at the bottom.
- Place all scripts/code in their respective folders (`sql/`, `scripts/`, etc.)
- Ensure all steps are fully **reproducible** using your documentation
- Create a new private repo and invite the reviewer https://github.com/mantreshjain

---

**Good luck! We look forward to your submission.**

## Solutions and Instructions (Filed by Candidate):

# ETL Pipeline - Job Assignment

## Project Summary

A complete ETL pipeline to process nested JSON data into a normalized MySQL schema, including data cleaning, transformation, and loading.

## Schema Design:

### Database: `home_db`

| Table       | Description                         | Primary Key   | Foreign Keys                |
| ----------- | ----------------------------------- | ------------- | --------------------------- |
| `property`  | Main property metadata              | `Property_ID` | -                           |
| `leads`     | Sales review and pipeline data      | `Property_ID` | FK → `property.Property_ID` |
| `hoa`       | HOA fees and flag indicators        | `id`          | FK → `property.Property_ID` |
| `valuation` | Market and rental pricing estimates | `id`          | FK → `property.Property_ID` |
| `rehab`     | Renovation and flag details         | `id`          | FK → `property.Property_ID` |

### Design Principles
Design Principles and Decisions:
Central Entity (property): This table serves as the anchor for all related data. Each record represents a distinct real estate listing. All other tables are dependent on this unique Property_ID.

One-to-One / One-to-Many Relationships:
Tables like leads, hoa, valuation, and rehab can have at most one corresponding record for each property. This reflects typical use-case where one property has one current valuation, one rehab scope, one HOA setting, and one lead record.

Use of Foreign Keys:
All dependent tables include foreign key constraints linking back to property. This ensures referential integrity and prevents orphan records.

Auto-Incrementing Primary Keys:
For non-central tables (rehab, hoa, valuation), the id column is used as the primary key, while Property_ID is maintained as a foreign key reference. This supports uniqueness within the table while linking to the main entity.

Storage Optimization:
TINYINT, SMALLINT, and FLOAT types are used to conserve storage while maintaining precision.
VARCHAR lengths are kept tight based on expected field length (e.g., State is 2 characters, Flood flags are short booleans).

Separation of Concerns:
By splitting data into specific tables (e.g., separating financial estimates into valuation, and renovation details into rehab), the schema is modular and supports easier updates and maintenance.

## How to Run the Scripts

### Prerequisites:
--MySQL Server 8.0
--Python 3.8+
--Database `home_db` must exist.

### Create Tables:
Run in order to preserve dependencies:

```bash
mysql -u <user> -p home_db < property_table.sql
mysql -u <user> -p home_db < lead_table.sql
mysql -u <user> -p home_db < hoa_table.sql
mysql -u <user> -p home_db < valuation_table.sql
mysql -u <user> -p home_db < rehab_table.sql
```

### Configure Environment

Edit `.env.development`:

```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=password
DB_NAME=home_db
```
## ETL Logic:

### File Overview
| File           | Description                                       |
| -------------- | ------------------------------------------------- |
| `main.py`      | Orchestrates the ETL pipeline                     |
| `extract.py`   | Loads JSON, flattens & explodes nested fields     |
| `transform.py` | Cleans data, splits into table-wise DataFrames    |
| `cleaner.py`   | Functions for null cleanup and type normalization |
| `database.py`  | Creates SQLAlchemy engine                         |
| `config.py`    | Loads environment and config paths                |

### Workflow:

1. **Extract**:
----JSON loaded via `extract.py`
----Nested fields (`Valuation`, `HOA`, `Rehab`) exploded

2. **Transform**:
-----`transform.py` applies cleaning:
       Replaces null-like values ("null", "NA", "None")
       Standardizes booleans ("Yes" → `True`)
       Fills categoricals with "Unknown"
       Fills numericals with median
       Field-to-table split driven by Excel config

3. **Load**:
------DataFrames loaded into MySQL using `to_sql()`

### Sample Cleaning Code (from `transform.py`):
```python
leads_df = replace_null_like_values(leads_df)
leads_df = fill_missing_categoricals(leads_df, ['Reviewed_Status', 'Source'])
```
## How to Run the Pipeline:

### Install Dependencies
```bash
pip install pandas openpyxl mysql-connector-python SQLAlchemy python-dotenv
```
### Run the Pipeline
```bash
python main.py
```
All five tables will be created and populated.

## Field Mapping
The `Field Config.xlsx` determines which fields go into which tables:
| Target Table | Example Fields                  |
| ------------ | ------------------------------- |
| `property`   | Address, State, SQFT\_Total     |
| `leads`      | Reviewed\_Status, IRR           |

## Requirements

| Component       | Version                   |
| --------------- | ------------------------- |
| Python          | 3.8+                      |
| MySQL           | 8.0+                      |
| pandas          | >=1.1.0                   |
| openpyxl        | For reading Excel config  |
| mysql-connector | DB connection backend     |
| SQLAlchemy      | ORM for MySQL             |
| python-dotenv   | For environment variables |

## Output
After running `main.py`, MySQL database `home_db` will be populated with cleaned and validated data across 5 related tables.


