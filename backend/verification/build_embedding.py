import os
import json
import joblib
import torch
from sentence_transformers import SentenceTransformer
from backend.ml.text_utils import clean_text

# =====================================================
# Paths
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA_FOLDER = os.path.join(BASE_DIR, "dataset", "raw", "rss")

MODEL_FOLDER = os.path.join(BASE_DIR, "backend", "models")

os.makedirs(MODEL_FOLDER, exist_ok=True)

# =====================================================
# Load all scraped articles
# =====================================================
articles = []
seen_keys = set()  # for deduplication (by URL, fallback to title)

filenames = sorted(
    f for f in os.listdir(DATA_FOLDER) if f.endswith(".json")
)

if not filenames:
    print(f"No .json files found in {DATA_FOLDER}. Nothing to do.")
    raise SystemExit(0)

for filename in filenames:
    path = os.path.join(DATA_FOLDER, filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"Skipping {filename}: failed to parse ({e})")
        continue

    if not isinstance(data, list):
        print(f"Skipping {filename}: expected a list of articles, got {type(data)}")
        continue

    for article in data:
        # dedupe key: prefer URL/GUID, fall back to title
        key = article.get("url") or article.get("link") or article.get("guid") or article.get("title")
        if not key:
            continue  # nothing to key on, skip malformed entry
        if key in seen_keys:
            continue
        seen_keys.add(key)
        articles.append(article)

print(f"Loaded {len(articles)} unique articles (from {len(filenames)} files).")

if not articles:
    print("No valid articles after parsing/deduplication. Nothing to embed.")
    raise SystemExit(0)

# =====================================================
# Prepare text
# =====================================================
documents = []
for article in articles:
    title = clean_text(article.get("title", ""))
    content = clean_text(article.get("content", ""))
    documents.append(f"{title}\n{content}")

# =====================================================
# Load Sentence Transformer
# =====================================================
print("\nLoading multilingual model...")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
print("Model loaded.\n")

# =====================================================
# Encode articles
# =====================================================
print("Encoding articles...")
embeddings = model.encode(
    documents,
    convert_to_tensor=True,
    show_progress_bar=True
)
print("Encoding complete.\n")

# =====================================================
# Save
# =====================================================
joblib.dump(articles, os.path.join(MODEL_FOLDER, "live_articles.pkl"))
torch.save(embeddings, os.path.join(MODEL_FOLDER, "live_embeddings.pt"))

print("Saved articles.")
print("Saved embeddings.")
print(f"\nDone. {len(articles)} articles embedded and saved to '{MODEL_FOLDER}'.")