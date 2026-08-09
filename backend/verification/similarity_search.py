import os
import joblib
import torch

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from backend.ml.text_utils import clean_text


# =====================================================
# Paths
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MODEL_DIR = os.path.join(BASE_DIR, "backend", "models")

ARTICLES_PATH = os.path.join(MODEL_DIR, "live_articles.pkl")
EMBEDDINGS_PATH = os.path.join(MODEL_DIR, "live_embeddings.pt")


# =====================================================
# Load model
# =====================================================

print("Loading Sentence Transformer...")

model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

print("Model loaded.")


# =====================================================
# Load search index
# =====================================================

print("Loading search index...")

articles = joblib.load(ARTICLES_PATH)

embeddings = torch.load(
    EMBEDDINGS_PATH,
    weights_only=False
)

print(f"{len(articles)} articles loaded.\n")


# =====================================================
# Search
# =====================================================

SIMILARITY_THRESHOLD = 0.90


def find_similar_articles(query,
                          top_k=5,
                          threshold=SIMILARITY_THRESHOLD):

    query = clean_text(query)

    if not query.strip():
        return []

    query_embedding = model.encode(
        query,
        convert_to_tensor=True
    )

    similarities = cos_sim(
        query_embedding,
        embeddings
    )[0]

    scores, indices = torch.topk(
        similarities,
        k=min(top_k, len(articles))
    )

    results = []

    for score, idx in zip(scores, indices):

        similarity = float(score)

        if similarity < threshold:
            continue

        results.append({
            "similarity": similarity,
            "article": articles[int(idx)]
        })

    return results


# =====================================================
# Test
# =====================================================

if __name__ == "__main__":

    query = input("Enter news:\n\n")

    results = find_similar_articles(query)

    if not results:

        print("\nNo similar articles found.")

    else:

        print()

        for result in results:

            article = result["article"]

            print("=" * 70)

            print(f"Similarity : {result['similarity']:.3f}")

            print("Source :", article["source"])

            print("Title :", article["title"])

            print("URL :", article["url"])

            print()