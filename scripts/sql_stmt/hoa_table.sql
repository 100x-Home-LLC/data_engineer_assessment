CREATE TABLE home_db.hoa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Property_ID SMALLINT,
    HOA INT,
    HOA_Flag VARCHAR(5),
    FOREIGN KEY (Property_ID) REFERENCES home_db.property(Property_ID)
);

