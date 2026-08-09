from datasets import load_dataset

# Load the dataset from Hugging Face
dataset = load_dataset("chhatramani/nepali-fake-news-dataset-v1")

# Display available splits
print(dataset)

# Convert the training split to a pandas DataFrame
df = dataset["train"].to_pandas()

# Show the first 5 rows
print(df.head())

# Save as CSV
df.to_csv("nepali_fake_news.csv", index=False, encoding="utf-8-sig")

print("Dataset saved successfully!")