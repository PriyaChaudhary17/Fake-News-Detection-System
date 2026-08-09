import os
import json
import pandas as pd

# =====================================================
# Paths
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

KAGGLE_DATASET = os.path.join(BASE_DIR, "dataset", "processed_data1.csv")

REAL_NEWS_JSON = os.path.join(
    BASE_DIR,
    "dataset",
    "processed",
    "real_news.json"
)

OUTPUT_DATASET = os.path.join(
    BASE_DIR,
    "dataset",
    "updated_training_dataset.csv"
)

# =====================================================
# Load Kaggle Dataset
# =====================================================

print("=" * 60)
print("Loading Kaggle Dataset...")
print("=" * 60)

kaggle_df = pd.read_csv(KAGGLE_DATASET)

print("Kaggle Articles:", len(kaggle_df))

# =====================================================
# Load Scraped News
# =====================================================

print("\nLoading Scraped News...")

with open(REAL_NEWS_JSON, "r", encoding="utf-8") as f:
    real_news = json.load(f)

print("Scraped Articles:", len(real_news))

# =====================================================
# Convert JSON into same format as Kaggle
# =====================================================

rows = []

for article in real_news:

    title = article.get("title", "").strip()

    content = article.get("content", "").strip()

    full_text = (title + " " + content).strip()

    if full_text == "":
        continue

    rows.append({

        "full_text": full_text,

        "label": 0        # REAL

    })

scraped_df = pd.DataFrame(rows)

print("Converted:", len(scraped_df))

# =====================================================
# Merge
# =====================================================

combined_df = pd.concat(
    [kaggle_df, scraped_df],
    ignore_index=True
)

print("\nMerged Articles:", len(combined_df))

# =====================================================
# Remove Duplicate News
# =====================================================

before = len(combined_df)

combined_df.drop_duplicates(
    subset=["full_text"],
    inplace=True
)

after = len(combined_df)

print(f"Duplicates Removed: {before-after}")

# =====================================================
# Shuffle
# =====================================================

combined_df = combined_df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# =====================================================
# Save
# =====================================================

combined_df.to_csv(
    OUTPUT_DATASET,
    index=False,
    encoding="utf-8-sig"
)

print("\n" + "=" * 60)
print("Training Dataset Updated Successfully")
print("=" * 60)
print("Final Dataset Size:", len(combined_df))
print("Saved to:", OUTPUT_DATASET)
print("\nLabel Distribution")
print(combined_df["label"].value_counts())