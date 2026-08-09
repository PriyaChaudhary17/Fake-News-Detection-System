import os
import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# ==========================
# Paths
# ==========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))

MODEL_DIR = os.path.join(PROJECT_DIR, "backend", "models")

# ==========================
# Load Preprocessed Data
# ==========================

X_train = joblib.load(os.path.join(MODEL_DIR, "X_train_tfidf.pkl"))
X_test = joblib.load(os.path.join(MODEL_DIR, "X_test_tfidf.pkl"))

y_train = joblib.load(os.path.join(MODEL_DIR, "y_train.pkl"))
y_test = joblib.load(os.path.join(MODEL_DIR, "y_test.pkl"))

encoder = joblib.load(os.path.join(MODEL_DIR, "label_encoder.pkl"))

print("Training label distribution:")
print(pd.Series(y_train).value_counts())
print("\nClass index mapping (from encoder.classes_):")
for cls, idx in zip(encoder.classes_, encoder.transform(encoder.classes_)):
    print(f"  {cls} -> {idx}")
print()

# ==========================
# Models
# ==========================
# class_weight="balanced" matters if your dataset is skewed toward one
# label (e.g. far more REAL articles than FAKE ones). Without it, the
# model can get a lower loss by just leaning toward the majority class.

models = {
    "Logistic Regression": LogisticRegression(
        solver="lbfgs",
        max_iter=5000,
        class_weight="balanced",
        C=1.0,
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced"
    ),

    "Naive Bayes": MultinomialNB(
        alpha=1.0
    ),

    "XGBoost": XGBClassifier(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=6,
        random_state=42,
        eval_metric="logloss",
        scale_pos_weight=(
            (pd.Series(y_train) == 0).sum() /
            max((pd.Series(y_train) == 1).sum(), 1)
        )
    )
}

# ==========================
# Training & Evaluation
# ==========================

results = []

best_accuracy = 0
best_f1 = 0
best_model = None
best_model_name = ""

print("=" * 60)
print("Training Models")
print("=" * 60)

for name, model in models.items():

    print(f"\nTraining {name}...")

    # Train
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="binary")
    recall = recall_score(y_test, y_pred, average="binary")
    f1 = f1_score(y_test, y_pred, average="binary")

    # Sample probability (debug)
    prob = model.predict_proba(X_test)[0]

    print("\nSample Prediction Probabilities:")
    print(prob)

    # Store results
    results.append([name, accuracy, precision, recall, f1])

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1-score : {f1:.4f}")

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print(classification_report(
        y_test,
        y_pred,
        target_names=[str(c) for c in encoder.classes_]
    ))

    # Save best model based on F1 Score
    if f1 > best_f1:
        best_f1 = f1
        best_accuracy = accuracy
        best_model = model
        best_model_name = name
# ==========================
# Results Table
# ==========================

results_df = pd.DataFrame(
    results,
    columns=["Model", "Accuracy", "Precision", "Recall", "F1"]
)

print("\n")
print("=" * 60)
print("Model Comparison")
print("=" * 60)
print(results_df)

# ==========================
# Save Best Model
# ==========================
print("\n")
print("=" * 60)
print("Best Model")
print("=" * 60)
print(f"Model    : {best_model_name}")
print(f"Accuracy : {best_accuracy:.4f}")
print(f"F1 Score : {best_f1:.4f}")

joblib.dump(
    best_model,
    os.path.join(MODEL_DIR, "text_model.pkl")
)

print("\nBest model saved as text_model.pkl")