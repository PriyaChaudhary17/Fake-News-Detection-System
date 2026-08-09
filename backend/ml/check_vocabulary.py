import os
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))

vectorizer = joblib.load(
    os.path.join(PROJECT_DIR, "backend", "models", "tfidf_vectorizer.pkl")
)

words = vectorizer.get_feature_names_out()

print("Vocabulary size:", len(words))

print("Contains समता ?", "समता" in words)

print("Contains कर ?", "कर" in words)

print("Contains शिक्षा ?", "शिक्षा" in words)