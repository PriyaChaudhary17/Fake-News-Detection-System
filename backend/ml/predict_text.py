import os
import sys
import re
import joblib


# ==========================================================
# Paths
# ==========================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from text_utils import clean_text


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(BASE_DIR)
MODEL_DIR = os.path.join(BACKEND_DIR, "models")


# ==========================================================
# Load Model
# ==========================================================

model = joblib.load(
    os.path.join(MODEL_DIR, "text_model.pkl")
)

vectorizer = joblib.load(
    os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
)


# ==========================================================
# Label Mapping
# ==========================================================
# Dataset:
#
# 0 = REAL
# 1 = FAKE
# ==========================================================

REAL_INDEX = 0
FAKE_INDEX = 1


# ==========================================================
# Validate News Input
# ==========================================================

def validate_news_text(text):
    """
    Check whether the input looks like a meaningful
    Nepali news article rather than random text,
    keywords, or a short phrase.
    """

    # ------------------------------------------------------
    # Empty input
    # ------------------------------------------------------

    if text is None or not str(text).strip():

        return False, "News text cannot be empty."


    text = str(text).strip()


    # ------------------------------------------------------
    # Must contain Nepali characters
    # ------------------------------------------------------

    nepali_chars = re.findall(
        r"[\u0900-\u097F]",
        text
    )

    if len(nepali_chars) < 10:

        return False, (
            "Please enter valid Nepali news text."
        )


    # ------------------------------------------------------
    # Split into words
    # ------------------------------------------------------

    words = text.split()

    if len(words) < 15:

        return False, (
            "Please enter a complete Nepali news article "
            "with at least 15 words."
        )


    # ------------------------------------------------------
    # Remove punctuation for word analysis
    # ------------------------------------------------------

    cleaned_words = []

    for word in words:

        word = word.strip(
            "।,!?()%/:\"'“”‘’-"
        )

        if word:
            cleaned_words.append(word)


    # ------------------------------------------------------
    # Check for keyword-list input
    # ------------------------------------------------------

    suspicious_words = {
        "दाबी",
        "गोप्य",
        "भाइरल",
        "तुरुन्त",
        "शेयर",
        "अफवाह",
        "१००%",
        "गारन्टी",
        "मनगढन्ते",
        "कपोलकल्पित",
        "भ्रामक",
        "अपुष्ट",
        "प्रमाणबिनाको",
        "अविश्वसनीय"
    }


    suspicious_count = sum(
        1
        for word in cleaned_words
        if word in suspicious_words
    )


    if len(cleaned_words) > 0:

        suspicious_ratio = (
            suspicious_count /
            len(cleaned_words)
        )

    else:

        suspicious_ratio = 0


    # If too much of the input is just
    # suspicious keywords, it is probably
    # not an actual news article.

    if suspicious_ratio >= 0.40:

        return False, (
            "The input appears to be a list of "
            "keywords rather than a complete news article."
        )


    # ------------------------------------------------------
    # Check sentence structure
    # ------------------------------------------------------

    sentence_endings = re.findall(
        r"[।!?]",
        text
    )


    # A longer text should normally contain
    # at least one sentence ending.

    if (
        len(sentence_endings) == 0
        and len(words) < 25
    ):

        return False, (
            "Please enter a complete news article "
            "with meaningful sentences."
        )


    # ------------------------------------------------------
    # Check repeated words
    # ------------------------------------------------------

    if len(cleaned_words) >= 10:

        unique_ratio = (
            len(set(cleaned_words))
            / len(cleaned_words)
        )

        if unique_ratio < 0.40:

            return False, (
                "The input does not appear to contain "
                "meaningful news content."
            )


    # ------------------------------------------------------
    # Valid
    # ------------------------------------------------------

    return True, ""


# ==========================================================
# Generate Prediction Reasons
# ==========================================================

def generate_reasons(
    text,
    prediction,
    confidence
):

    reasons = []


    suspicious_words = [
        "फेक",
        "झुटो",
        "अफवाह",
        "भ्रामक",
        "अपुष्ट",
        "प्रमाणबिनाको",
        "मनगढन्ते",
        "कपोलकल्पित",
        "हल्ला",
        "दाबी",
        "भाइरल",
        "गोप्य",
        "तुरुन्त",
        "शेयर",
        "चमत्कार",
        "अविश्वसनीय",
        "१००%",
        "गारन्टी"
    ]


    # ------------------------------------------------------
    # Find suspicious words
    # ------------------------------------------------------

    found = []

    for word in suspicious_words:

        if word in text and word not in found:

            found.append(word)


    if found:

        reasons.append(
            "Possible misinformation-related words "
            "detected: "
            + ", ".join(found)
        )


    # ------------------------------------------------------
    # Model confidence explanation
    # ------------------------------------------------------

    if confidence < 65:

        reasons.append(
            "The model confidence is moderate. "
            "Verify the information using trusted news sources."
        )

    elif prediction == "REAL":

        reasons.append(
            "The trained ML model classified the "
            "news as REAL."
        )

    elif prediction == "FAKE":

        reasons.append(
            "The trained ML model classified the "
            "news as FAKE."
        )


    return reasons


# ==========================================================
# Prediction Function
# ==========================================================

def predict_news(news_text):


    # ======================================================
    # 1. Validate Input
    # ======================================================

    is_valid, validation_message = validate_news_text(
        news_text
    )


    if not is_valid:

        raise ValueError(
            validation_message
        )


    # ======================================================
    # 2. Clean Text
    # ======================================================

    cleaned_text = clean_text(
        news_text
    )


    if cleaned_text == "":

        raise ValueError(
            "No meaningful text remained after preprocessing."
        )


    print("\nCleaned Text:")
    print(cleaned_text)


    # ======================================================
    # 3. Check Word Count After Cleaning
    # ======================================================

    words = cleaned_text.split()


    if len(words) < 5:

        raise ValueError(
            "Please enter a complete Nepali news article."
        )


    # ======================================================
    # 4. TF-IDF
    # ======================================================

    text_vector = vectorizer.transform(
        [cleaned_text]
    )


    # ======================================================
    # 5. Check Vocabulary Match
    # ======================================================

    if text_vector.nnz == 0:

        raise ValueError(
            "The entered text does not contain "
            "recognized words from the trained vocabulary."
        )


    # ======================================================
    # 6. Debug Detected Features
    # ======================================================

    feature_names = (
        vectorizer.get_feature_names_out()
    )

    indices = text_vector.nonzero()[1]


    print("\nDetected Words:")

    for i in indices:

        print(
            "•",
            feature_names[i]
        )


    # ======================================================
    # 7. Model Prediction
    # ======================================================

    prediction = int(
        model.predict(
            text_vector
        )[0]
    )


    probabilities = model.predict_proba(
        text_vector
    )[0]


    # ======================================================
    # 8. Probabilities
    # ======================================================

    real_probability = float(
        probabilities[REAL_INDEX] * 100
    )

    fake_probability = float(
        probabilities[FAKE_INDEX] * 100
    )


    confidence = float(
        max(
            real_probability,
            fake_probability
        )
    )


    # ======================================================
    # 9. Convert Prediction to Label
    # ======================================================

    if prediction == REAL_INDEX:

        label = "REAL"

    elif prediction == FAKE_INDEX:

        label = "FAKE"

    else:

        raise ValueError(
            "Model returned an unknown class."
        )


    # ======================================================
    # 10. Print Result
    # ======================================================

    print("\nRaw Model Prediction:")
    print(prediction)

    print("\nModel Probabilities:")
    print(
        "REAL:",
        round(real_probability, 2),
        "%"
    )

    print(
        "FAKE:",
        round(fake_probability, 2),
        "%"
    )

    print(
        "\nFINAL LABEL:",
        label
    )

    print(
        "CONFIDENCE:",
        round(confidence, 2)
    )


    # ======================================================
    # 11. Generate Reasons
    # ======================================================

    reasons = generate_reasons(
        cleaned_text,
        label,
        confidence
    )


    # ======================================================
    # 12. Return Result
    # ======================================================

    return {

        "prediction": label,

        "confidence": round(
            confidence,
            2
        ),

        "real_probability": round(
            real_probability,
            2
        ),

        "fake_probability": round(
            fake_probability,
            2
        ),

        "reasons": reasons

    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    print("=" * 50)
    print("Nepali Fake News Detection")
    print("=" * 50)


    news = input(
        "\nEnter Nepali News:\n\n"
    )


    try:

        result = predict_news(
            news
        )


        print("\nPrediction Result")
        print("-" * 30)


        print(
            "Prediction       :",
            result["prediction"]
        )


        print(
            "Confidence       :",
            result["confidence"],
            "%"
        )


        print(
            "REAL Probability :",
            result["real_probability"],
            "%"
        )


        print(
            "FAKE Probability :",
            result["fake_probability"],
            "%"
        )


        print("\nReasons")
        print("-" * 30)


        for reason in result["reasons"]:

            print(
                "•",
                reason
            )


    except Exception as e:

        print(
            "\nError:",
            e
        )