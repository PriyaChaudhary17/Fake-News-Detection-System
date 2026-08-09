import pandas as pd

df = pd.read_csv("dataset/processed_data.csv")

print(df.columns)
print(df.head())