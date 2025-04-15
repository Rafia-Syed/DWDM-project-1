

# # Remove null values
# df.dropna(inplace=True)

# # Remove ₹ and commas from Price column and convert to int
# df['Price'] = df['Price'].replace('[₹,]', '', regex=True).astype(int)

# # Clean Ram column (e.g., "8 GB" → 8)
# df['Ram'] = df['Ram'].str.replace('GB', '').astype(int)

# print(df.columns)