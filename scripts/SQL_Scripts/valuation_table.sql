CREATE TABLE home_db.valuation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Property_ID SMALLINT,
    List_Price FLOAT,
    Previous_Rent FLOAT,
    ARV FLOAT,
    Rent_Zestimate FLOAT,
    Low_FMR FLOAT,
    Redfin_Value FLOAT,
    Zestimate FLOAT,
    Expected_Rent FLOAT,
    High_FMR FLOAT,
    FOREIGN KEY (Property_ID) REFERENCES home_db.property(Property_ID)
);

