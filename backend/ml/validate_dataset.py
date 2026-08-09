import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))

DATASET_PATH = os.path.join(PROJECT_DIR, "dataset", "processed_data.csv")

df = pd.read_csv(DATASET_PATH)

print("=" * 50)
print("DATASET VALIDATION REPORT")
print("=" * 50)

print("\nTotal Samples:")
print(len(df))

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate News:")
print(df.duplicated(subset="full_text").sum())

print("\nLabel Distribution:")
print(df["label"].value_counts())

print("\nCategory Distribution:")
print(df["category"].value_counts())

print("\nUnique Labels:")
print(df["label"].unique())

print("\nRandom REAL News:")
print(df[df["label"] == 1][["headline"]].sample(5))

print("\nRandom FAKE News:")
print(df[df["label"] == 0][["headline"]].sample(5))

print("\nValidation Completed Successfully!")