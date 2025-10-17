--creatted database home_db
create database home_db;
use home_db;

--created the table property as per the xl sheet
--using property id as a auto_increment primary key

create table property(
property_id int not null auto_increment primary key,
Property_Title  varchar(200),
Address varchar(200),
Market varchar(200),
Flood varchar(200),
Street_Address varchar(200),
City varchar(200),
State varchar(200),
Zip  int,
Property_Type varchar(200),
Highway varchar(200),
Train varchar(200),
Tax_Rate decimal(10,2),
SQFT_Basement int,
HTW varchar(200),
Pool varchar(200),
Commercial varchar(200),
Water varchar(200),
Sewage varchar(200),
Year_Built int,
SQFT_MU int,
SQFT_Total int,
Parking varchar(200),
Bed   int,
Bath int,
BasementYesNo varchar(200),
Layout varchar(200),
Rent_Restricted varchar(200),
Neighborhood_Rating int,
Latitude decimal(10,2),
Longitude  decimal(10,2),
Subdivision varchar(200),
Taxes   int,
School_Average decimal(10,2));

--created the table leads as per the xl sheet
--using lead id as a auto_increment primary key
-- leads table use property_id from property table as foreign key

create table leads(
leads_id int not null auto_increment primary key,
Reviewed_Status varchar(200),
Most_Recent_Status varchar(200),
Source varchar(200),
Occupancy varchar(200),
Net_Yield varchar(200),
IRR varchar(200),
Selling_Reason varchar(200),
Seller_Retained_Broker varchar(200),
Final_Reviewer varchar(200),
foreign key (leads_id) references property (property_id));

select count(*) from leads;

select * from leads limit 10;

select count(*) from property;

select* from  property limit 5;  
  
----taxes table is created using the fields
  
create table taxes(
	Taxes_id int not null primary key auto_increment,
	Taxes int);
    
select count(*) from taxes;

--created the table valuation as per the xl sheet
--using valuation_id as a auto_increment primary key
 
 create table valuation(
 Valuation_id int not null primary key auto_increment,
 List_Price	int,
 Previous_Rent decimal(10,2),	
 ARV	decimal(10,2),
 Rent_Zestimate	decimal(10,2),
 Low_FMR decimal(10,2),	
 Redfin_Value	decimal(10,2),
 Zestimate decimal(10,2),	
 Expected_Rent	decimal(10,2),
 High_FMR decimal(10,2));
 show create table valuation;
 
 select count(*) from valuation; -- 24705
 
 select * from valuation limit 10;

 --created the table rehab as per the xl sheet
--using rehab_id as a auto_increment primary key
-- rehab table use valuation_id from valuation table as foreign key
 create table rehab(
 Rehab_id int not null primary key auto_increment,
 Underwriting_Rehab	int,
 Rehab_Calculation varchar(50),	
 Paint	varchar(50),
 Flooring_Flag	varchar(50),
 Foundation_Flag varchar(50),	
 Roof_Flag	varchar(50),
 HVAC_Flag	varchar(50),
 Kitchen_Flag varchar(50),	
 Bathroom_Flag	varchar(50),
 Appliances_Flag varchar(50),	
 Windows_Flag	varchar(50),
 Landscaping_Flag varchar(50),	
 Trashout_Flag varchar(50),
 foreign key (Rehab_id) references valuation (valuation_id));
 
--hoa table is created
create table hoa(
HOA_id int not null primary key auto_increment,
HOA int,
HOA_Flag varchar(100));

select * from hoa;
select count(*) from rehab;
select * from hoa limit 10;
