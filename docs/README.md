

### Steps i have followed

- Used mysql workbench -8.0.43
- used jupyterNotebook - 8.0.43

### Python
  - have used pandas library 
  - fetched the json file using DataFrame
  - make connection with the mysql workbench using necessory install mysql-connector-python
  - After connection is established , i fetch required columns and clean the data
    Remove duplicates
  - And for the nested datas in json file, performs normalization using pd.json_normalize
  - Have created variable for source file and used in normalization
  - then load the data to the created table in Mysql 
  - Likewise loaded all the required datas to the concern table
    and close the connection to the Mysql

---

## Mysql
- As the Docker is not working in my system due to space issue i have created the given
  database in my local system and created given target tables with required data types 
  as in the excel sheet 
- And i have given required primary and foreign key constrain to the required fields
- then datas is pushed from Python , then i check count of the tables


**I have uploaded all the .sql and .py files with the exported table dada from mysql **


