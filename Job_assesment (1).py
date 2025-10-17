#!/usr/bin/env python
# coding: utf-8

# In[1]:


# install pandas 
pip install pandas 


# In[2]:


# install pymysql
pip install pymysql


# In[7]:


# install sqlalchemy
pip install sqlalchemy


# In[8]:


# install mysql-connector-python
pip install mysql-connector-python


# In[14]:


# importing required files

import pandas as pd
import pymysql
import json
from sqlalchemy import create_engine


# In[6]:


# read the .json file
df = pd.read_json("fake_property_data.json")
print(df)


# In[10]:


# connect python with Mysql in the local host using Mysql-connector
import mysql.connector

mydb = mysql.connector.connect(host = 'localhost',user = 'root',password = 'root123four')

if mydb.is_connected():
    print('connection established....')


# In[11]:


# create engine
engine=create_engine('mysql+pymysql://root:root123four@localhost/home_db')


# In[12]:


#json file as DataFrame
df = pd.read_json("fake_property_data.json")
df


# In[21]:


df.head(5)


# In[ ]:


print(df.columns)


# In[ ]:


Valuation_column =['Valuation']
view_column = df[Valuation_column]
print(view_column)


# In[16]:


# Assign variable to the file name
try:
    with open('fake_property_data.json', 'r') as f:
        data_to_normalize = json.load(f)
except FileNotFoundError:
    print("Error: The file 'fake_property_data.json' was not found.")
    exit()


# In[17]:


# normalize the datas in the column Valuation
df_val = pd.json_normalize(
    data_to_normalize,
    record_path='Valuation'
)

# Drop duplicate rows
df_val_unique = df_val.drop_duplicates()

# Display the resulting DataFrame without duplicates
print(df_val_unique)


# In[ ]:


# export the valuation datas to the Mysql table
df_val_unique.to_sql('valuation',engine,if_exists='append',index=False)
print ('data has been exported...')


# In[ ]:


Rehab_column =['Rehab']
view_column = df[Rehab_column]
view_column


# In[19]:


#Flattend the datas in the rehab column
df_Rehab = pd.json_normalize(
    data_to_normalize, 
    record_path='Rehab'
)
# Drop duplicate rows
df_Rehab_unique = df_Rehab.drop_duplicates()
df_Rehab_unique


# In[ ]:


# exported the datas in the rehab column to the mysql table
df_Rehab_unique.to_sql('rehab',engine,if_exists='append',index=False)
print ('data has been exported...')


# In[ ]:


df_hoa=['HOA']
view_hoa = df[df_hoa]
view_hoa


# In[20]:


# Flattend the datas in the HOA column 
df_hoa = pd.json_normalize(
    data_to_normalize,  # <- Use the defined variable
    record_path='HOA'
)
# Drop duplicate rows
df_hoa_unique = df_hoa.drop_duplicates()
df_hoa_unique


# In[ ]:


# exported the datas in the HOA column toe the mysql table
df_hoa_unique.to_sql('hoa',engine,if_exists='append',index=False)
print ('data has been exported...')


# In[ ]:


# find the datatype of specified columns

Leads_column =['Reviewed_Status', 'Most_Recent_Status',
       'Source','Occupancy','Net_Yield', 'IRR','Selling_Reason', 'Seller_Retained_Broker','Final_Reviewer']
column_dtypes = df[Leads_column].dtypes

print(column_dtypes)


# In[ ]:


Leads_column =['Reviewed_Status', 'Most_Recent_Status',
       'Source','Occupancy','Net_Yield', 'IRR','Selling_Reason', 'Seller_Retained_Broker','Final_Reviewer']
columns= df[Leads_column]

print(columns)


# In[ ]:


# Drop duplicate rows
columns_unique = columns.drop_duplicates()
columns_unique

# exported the datas in the leads column to the mysql table
columns_unique.to_sql('leads',engine,if_exists='append',index=False)
print ('data has been exported...')


# In[ ]:


Taxes_column =['Taxes']
column_Taxes= df[Taxes_column]

print(column_Taxes)


# In[ ]:


# Drop duplicate rows
Taxes_unique = column_Taxes.drop_duplicates()
Taxes_unique

# exported the datas in the Taxes column to the mysql table
Taxes_unique.to_sql('taxes',engine,if_exists='append',index=False)
print ('data has been exported...')


# In[ ]:


# find the datatype of specified property columns

property_column =['Property_Title', 'Address',
        'Market', 'Flood', 'Street_Address', 'City',
       'State', 'Zip', 'Property_Type', 'Highway', 'Train', 'Tax_Rate',
       'SQFT_Basement', 'HTW', 'Pool', 'Commercial', 'Water', 'Sewage',
       'Year_Built', 'SQFT_MU', 'SQFT_Total', 'Parking', 'Bed', 'Bath',
       'BasementYesNo', 'Layout', 'Rent_Restricted',
       'Neighborhood_Rating', 'Latitude', 'Longitude', 'Subdivision',
       'School_Average']
column_dtypes = df[property_column].dtypes

print(column_dtypes)


# In[ ]:




property_column =['Property_Title', 'Address',
        'Market', 'Flood', 'Street_Address', 'City',
       'State', 'Zip', 'Property_Type', 'Highway', 'Train', 'Tax_Rate',
       'SQFT_Basement', 'HTW', 'Pool', 'Commercial', 'Water', 'Sewage',
       'Year_Built', 'SQFT_MU', 'SQFT_Total', 'Parking', 'Bed', 'Bath',
       'BasementYesNo', 'Layout', 'Rent_Restricted',
       'Neighborhood_Rating', 'Latitude', 'Longitude', 'Subdivision',
       'School_Average']
columns_property= df[property_column]

print(columns_property)


# In[ ]:


# Drop duplicate rows
property_unique = columns_property.drop_duplicates()
property_unique

# exported the datas in the property column to the mysql table
property_unique.to_sql('property',engine,if_exists='append',index=False)
print ('data has been exported...')


# In[ ]:


property_unique.head(5)


# In[ ]:


# close engine
engine.dispose()

