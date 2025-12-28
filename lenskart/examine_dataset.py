"""Script to examine the dataset structure."""
import pandas as pd

# Read the Xl file
df = pd.read_excel('A1.0_data_product_images.xlsx')

# Print basic information
print("=" * 50)
print("DATASET EXPLORATION")
print("=" * 50)
print(f"\nShape: {df.shape} (rows, columns)")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nData types:\n{df.dtypes}")
print("\n" + "=" * 50)
print("First 5 rows:")
print("=" * 50)
print(df.head())

print("\n" + "=" * 50)
print("Dataset Info:")
print("=" * 50)
print(df.info())

print("\n" + "=" * 50)
print("Sample data (first row details):")
print("=" * 50)
if len(df) > 0:
    for col in df.columns:
        print(f"{col}: {df[col].iloc[0]}")

print("\n" + "=" * 50)
print("Null values:")
print("=" * 50)
print(df.isnull().sum())

