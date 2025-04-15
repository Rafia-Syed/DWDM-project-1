import pandas as pd
from sqlalchemy import create_engine

# Load your cleaned dataset
df = pd.read_csv("Cleaned_Laptop_Data.csv")

# Create a connection to SQLite (this will create a file 'laptops.db')
engine = create_engine('sqlite:///laptops.db', echo=False)

# Push the DataFrame to the SQLite DB as a table called 'laptops'
df.to_sql('laptops', con=engine, if_exists='replace', index=False)

print("Data successfully pushed to SQLite DW simulation (laptops.db)")
