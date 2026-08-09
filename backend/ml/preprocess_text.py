from json import encoder
import os
import sys
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

# ==========================
# Import shared cleaning function
# ==========================
# text_utils.py must live somewhere importable (e.g. backend/ or project root).
# Adjust sys.path below if your folder layout differs.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
BACKEND_DIR = os.path.join(PROJECT_DIR, "backend")

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from text_utils import clean_text  # noqa: E402  (same function used at inference)

# ==========================
# Configuration
# ==========================
MAX_FEATURES = 10000
TEST_SIZE = 0.2
RANDOM_STATE = 42


# ==========================
# Paths
# ==========================

DATASET_PATH = os.path.join(PROJECT_DIR, "dataset", "processed_data1.csv")
MODEL_DIR = os.path.join(PROJECT_DIR, "backend", "models")

os.makedirs(MODEL_DIR, exist_ok=True)


# ==========================
# Main Preprocessing Function
# ==========================

def preprocess():

    # Load dataset
    df = pd.read_csv(DATASET_PATH)

    # Keep required columns
    df = df[["full_text", "label"]]

    # Remove missing values
    df.dropna(inplace=True)

    # ---- Sanity check on label balance BEFORE encoding ----
    print("Raw label distribution:")
    print(df["label"].value_counts())
    print()

    # Clean text (identical function used later at inference time)
    df["full_text"] = df["full_text"].apply(clean_text)

    # Remove empty rows (this can happen more often now since cleaning
    # is more aggressive - Devanagari-only). Worth knowing if it guts
    # a large fraction of one class.
    before_empty = len(df)
    df = df[df["full_text"].str.strip().astype(bool)]
    after_empty = len(df)
    if before_empty != after_empty:
        print(f"Rows dropped for empty text after cleaning: {before_empty - after_empty}")

    # Remove duplicates
    before = len(df)
    df.drop_duplicates(subset="full_text", inplace=True)
    after = len(df)

    # Encode labels
    encoder = LabelEncoder()
    df["label"] = encoder.fit_transform(df["label"])

    joblib.dump(
        encoder,
        os.path.join(MODEL_DIR, "label_encoder.pkl")
    )
    # ==========================
# Debug Label Information
# ==========================

    print("\nLabel Distribution After Encoding")
    print(df["label"].value_counts())

    print("\nEncoded Label Mapping")
    for cls, idx in zip(
            encoder.classes_,
            encoder.transform(encoder.classes_)
    ):
        print(f"{cls} -> {idx}")

    # Features & Labels
    X = df["full_text"]
    y = df["label"]

    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )

    # TF-IDF
    vectorizer = TfidfVectorizer(
    max_features=MAX_FEATURES,
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True,
    lowercase=False
    )

    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Save vectorizer
    joblib.dump(
        vectorizer,
        os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
    )

    # Save processed data
    joblib.dump(X_train_tfidf, os.path.join(MODEL_DIR, "X_train_tfidf.pkl"))
    joblib.dump(X_test_tfidf, os.path.join(MODEL_DIR, "X_test_tfidf.pkl"))
    joblib.dump(y_train, os.path.join(MODEL_DIR, "y_train.pkl"))
    joblib.dump(y_test, os.path.join(MODEL_DIR, "y_test.pkl"))

    # Information
    print("=" * 50)
    print("Dataset Loaded Successfully")
    print("=" * 50)

    print(f"Duplicates Removed : {before - after}")
    print(f"Total Samples      : {len(df)}")
    print(f"Training Samples   : {X_train.shape[0]}")
    print(f"Testing Samples    : {X_test.shape[0]}")
    print(f"TF-IDF Features    : {X_train_tfidf.shape[1]}")

    print("\nLabel Mapping (verify this matches what predict.py expects!):")
    for label, value in zip(
        encoder.classes_,
        encoder.transform(encoder.classes_)
    ):
        print(f"{label} -> {value}")

    print("\nPreprocessing Completed Successfully!")

    return (
        X_train_tfidf,
        X_test_tfidf,
        y_train,
        y_test
    )


# ==========================
# Run Script
# ==========================

if __name__ == "__main__":
    preprocess()