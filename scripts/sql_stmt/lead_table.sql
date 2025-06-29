CREATE TABLE home_db.leads (
  `Property_ID` SMALLINT,
  `Reviewed_Status` VARCHAR(14),
  `Most_Recent_Status` VARCHAR(11),
  `Source` VARCHAR(11),
  `Occupancy` VARCHAR(3),
  `Net_Yield` FLOAT,
  `IRR` FLOAT,
  `Selling_Reason` VARCHAR(13),
  `Seller_Retained_Broker` VARCHAR(3),
  `Final_Reviewer` VARCHAR(15),
  PRIMARY KEY (`Property_ID`)
);
