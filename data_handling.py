import pandas as pd
import numpy as np
import re

# Load the dataset
df = pd.read_csv('laptopData.csv')
print(df.head())

# Remove null values
df.dropna(inplace=True)

# Remove ₹ and commas from Price column and convert to int
df['Price'] = df['Price'].replace('[₹,]', '', regex=True).astype(int)

# Clean Ram column (e.g., "8 GB" → 8)
df['Ram'] = df['Ram'].str.replace('GB', '').astype(int)

# Clean Weight column
df['Weight'] = df['Weight'].str.replace('kg', '').str.strip()
df['Weight'] = pd.to_numeric(df['Weight'], errors='coerce')  # convert to float

# Extract CPU Brand
df['CPU_Brand'] = df['Cpu'].apply(lambda x: x.split()[0])

# Extract Touchscreen and IPS info
df['Touchscreen'] = df['ScreenResolution'].apply(lambda x: 1 if 'Touchscreen' in x else 0)
df['IPS'] = df['ScreenResolution'].apply(lambda x: 1 if 'IPS' in x else 0)

# Extract resolution (X_res and Y_res)
def extract_resolution(x):
    res = re.findall(r'(\d+)x(\d+)', x)
    if res:
        return int(res[0][0]), int(res[0][1])
    else:
        return None, None

df['X_res'], df['Y_res'] = zip(*df['ScreenResolution'].map(extract_resolution))

# Clean Inches column
df['Inches'] = df['Inches'].str.strip()
df['Inches'] = pd.to_numeric(df['Inches'], errors='coerce')
df.dropna(subset=['Inches'], inplace=True)
df['Inches'] = df['Inches'].astype(float)

# Calculate PPI (Pixels Per Inch)
df['PPI'] = ((df['X_res']**2 + df['Y_res']**2) ** 0.5) / df['Inches']

# Clean and transform Memory column
df['Memory'] = df['Memory'].str.replace('GB', '').str.replace('TB', '000')
df['Memory'] = df['Memory'].str.replace('+', ' ')
df['Memory'] = df['Memory'].str.replace('.', '')  # remove stray dots
df['Memory'] = df['Memory'].str.strip()

# Initialize default values
df['SSD'] = 0
df['HDD'] = 0

# Function to extract SSD and HDD values
def extract_storage(mem):
    mem = mem.upper()
    ssd = 0
    hdd = 0
    parts = mem.split()
    for i in range(len(parts)):
        if 'SSD' in parts[i]:
            ssd = int(re.sub(r'\D', '', parts[i-1]))
        elif 'HDD' in parts[i]:
            hdd = int(re.sub(r'\D', '', parts[i-1]))
    return pd.Series([ssd, hdd])

df[['SSD', 'HDD']] = df['Memory'].apply(extract_storage)

# Use NumPy to create a new feature (log price)
df['Log_Price'] = np.log(df['Price'])

# Save cleaned data
df.to_csv("Cleaned_Laptop_Data.csv", index=False)

# Uncomment to view summary
# print(df.columns)
# print(df.info())
