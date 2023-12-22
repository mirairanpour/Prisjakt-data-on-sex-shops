
import pandas as pd
import sqlite3


# Loading our data from the excel file  
df = pd.read_csv('prisjakt data.csv')

# cleaning our data after importing it.
# some coloumns have a lottttt of missing values so we will get rid of those columns 
threshold = 0.5  # columns that have more than 50% missing values will be dropped
df_cleaned = df.dropna(thresh=len(df) * threshold, axis=1)

# there are two columns, one has price and one price with shipping. there are a lot of missing values in the price with shipping so we replace it with the price column, the difference shouldn't be huge, it's usually less than 100 kroner
df_cleaned['PriceIncShipping'].fillna(df_cleaned['Price'], inplace=True)

# using convert_dtypes method to automatically convert the data types to the best one
df_cleaned = df_cleaned.convert_dtypes()

# removing the rows which are duplicates
df_cleaned = df_cleaned.drop_duplicates()

# some columns have titles that might not be so good in a database so we replace them with '_'
df_cleaned.columns = df_cleaned.columns.str.replace('[^A-Za-z0-9]+', '_', regex=True)

# finally we will load the data that we cleaned into the snowflake database. 
con2 = sqlite3.connect("db")
df_cleaned.to_sql("prisjakt",con2,if_exists="replace")