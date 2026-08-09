"""
Run this after preprocess.py to diagnose prediction bias.
Paste the full output back for further help.
"""

import os
import joblib
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
MODEL_DIR = os.path.join(PROJECT_DIR, "backend", "models")

encoder = joblib.load(os.path.join(MODEL_DIR, "label_encoder.pkl"))
y_train = joblib.load(os.path.join(MODEL_DIR, "y_train.pkl"))
y_test = joblib.load(os.path.join(MODEL_DIR, "y_test.pkl"))
X_test = joblib.load(os.path.join(MODEL_DIR, "X_test_tfidf.pkl"))

print("=" * 60)
print("1. CLASS BALANCE")
print("=" * 60)
print("encoder.classes_ :", list(encoder.classes_))
print("\nTrain label counts:")
print(pd.Series(y_train).value_counts())
print("\nTest label counts:")
print(pd.Series(y_test).value_counts())

ratio = pd.Series(y_train).value_counts(normalize=True)
print(f"\nTrain class ratio:\n{ratio}")
if ratio.max() > 0.65:
    print("\n>>> WARNING: Significant class imbalance detected. This is a "
          "very likely cause of the model always predicting the majority "
          "class. See scale_pos_weight suggestion below.")

print("\n" + "=" * 60)
print("2. MODEL BEHAVIOR ON TEST SET")
print("=" * 60)

model = joblib.load(os.path.join(MODEL_DIR, "text_model.pkl"))
y_pred = model.predict(X_test)

print("Predicted label counts on test set:")
print(pd.Series(y_pred).value_counts())

from sklearn.metrics import f1_score, classification_report, confusion_matrix

print("\nF1 score (per class):")
print(f1_score(y_test, y_pred, average=None))
print("Classes order:", encoder.classes_)

print("\nFull classification report:")
print(classification_report(y_test, y_pred, target_names=[str(c) for c in encoder.classes_]))

print("\nConfusion matrix (rows=actual, cols=predicted):")
print(confusion_matrix(y_test, y_pred))

if hasattr(model, "predict_proba"):
    probs = model.predict_proba(X_test)
    print("\nAverage predicted probability per class across ALL test samples:")
    print(probs.mean(axis=0))
    print(">>> If one column's average is much higher regardless of true "
          "label, the model itself is biased (not just borderline cases).")

# scale_pos_weight suggestion for XGBoost, if imbalance found
counts = pd.Series(y_train).value_counts()
if len(counts) == 2:
    majority = counts.max()
    minority = counts.min()
    print(f"\nSuggested XGBoost scale_pos_weight = {majority/minority:.3f}")
    print("(set this in the XGBClassifier(...) constructor in train.py)")