import json
import os

from sentence_transformers import SentenceTransformer, util

# =====================================================
# Paths
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))

DATABASE = os.path.join(
    PROJECT_DIR,
    "dataset",
    "verified_news.json"
)

# =====================================================
# Load Database
# =====================================================

print("Loading database...")

with open(DATABASE, "r", encoding="utf-8") as f:
    database = json.load(f)

print(f"Loaded {len(database)} articles.")

# =====================================================
# Load Semantic Model
# =====================================================

print("\nLoading multilingual model...")

model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

print("Model loaded successfully!")

# =====================================================
# Encode Articles
# =====================================================

documents = []

for article in database:

    title = article.get("title", "")
    content = article.get("content", "")

    documents.append(title + "\n" + content)

print("\nEncoding articles...")

document_embeddings = model.encode(
    documents,
    convert_to_tensor=True,
    show_progress_bar=True
)

print("Encoding complete!")

# =====================================================
# Semantic Search
# =====================================================

def find_similar_articles(query, top_k=5):

    query_embedding = model.encode(
        query,
        convert_to_tensor=True
    )

    similarities = util.cos_sim(
        query_embedding,
        document_embeddings
    )[0]

    top_results = similarities.topk(k=top_k)

    results = []

    for score, index in zip(top_results.values, top_results.indices):

        results.append({
            "similarity": float(score),
            "article": database[int(index)]
        })

    return results


# =====================================================
# Test
# =====================================================

if __name__ == "__main__":

    query = input("Enter news:\n\n")

    results = find_similar_articles(query)

    print()

    if not results:
        print("No similar articles found.")

    else:

        for result in results:

            article = result["article"]

            print("=" * 60)
            print(f"Similarity : {result['similarity']:.3f}")
            print("Source :", article.get("source", "N/A"))
            print("Title :", article.get("title", "N/A"))
            print("URL :", article.get("url", "N/A"))