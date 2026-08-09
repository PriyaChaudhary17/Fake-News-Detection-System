import json
import logging

from backend.verification.url_verifier import is_url, verify_url
from backend.verification.search_database import (
    load_database,
    search_by_title,
    search_by_content,
)
from backend.verification.similarity_search import find_similar_articles
from backend.ml.predict_text import predict_news

logger = logging.getLogger(__name__)

MIN_QUERY_LENGTH = 6
SIMILARITY_THRESHOLD = 0.45

database = load_database()


def trim_article(article):
    return {
        "title": article.get("title", "N/A"),
        "url": article.get("url", "N/A"),
        "source": article.get("source", "N/A"),
        "published": article.get("published", "N/A"),
    }


def verify_news(user_input):

    user_input = user_input.strip()

    if not user_input:
        return {
            "verified": False,
            "method": "Empty Input",
            "matches": []
        }

    # ---------------------------------------
    # URL INPUT
    # ---------------------------------------

    if is_url(user_input):

        scraped = verify_url(user_input)

        if scraped.get("verified") is False:
            scraped.setdefault("matches", [])
            scraped.setdefault("method", "URL Verification Failed")
            return scraped

        title = scraped.get("title", "")
        content = scraped.get("content", "")

    else:

        title = user_input
        content = user_input

    if len(content) < MIN_QUERY_LENGTH:
        return {
            "verified": False,
            "method": "Input Too Short",
            "matches": []
        }

    verification = None

    # ---------------------------------------
    # DATABASE TITLE SEARCH
    # ---------------------------------------

    try:

        title_matches = search_by_title(database, title)

        if title_matches:

            verification = {
                "verified": True,
                "method": "Database Title Match",
                "matches": [
                    trim_article(a)
                    for a in title_matches[:5]
                ]
            }

    except Exception:
        logger.exception("Title search failed")

    # ---------------------------------------
    # SIMILARITY SEARCH
    # ---------------------------------------

    if verification is None:

        try:

            similar = find_similar_articles(content)

            if similar:

                best = similar[0]

                if best["similarity"] >= SIMILARITY_THRESHOLD:

                    verification = {
                        "verified": True,
                        "method": "Similarity Match",
                        "similarity": round(best["similarity"], 3),
                        "matches": [
                            trim_article(best["article"])
                        ]
                    }

        except Exception:
            logger.exception("Similarity search failed")

    # ---------------------------------------
    # ALWAYS RUN ML
    # ---------------------------------------

    try:

        prediction = predict_news(content)

    except Exception:

        logger.exception("Prediction failed")

        prediction = {
            "prediction": "UNKNOWN",
            "confidence": 0,
            "real_probability": 0,
            "fake_probability": 0
        }

    # ---------------------------------------
    # RETURN RESULT
    # ---------------------------------------

    if verification:

        verification["prediction"] = prediction

        return verification

    return {
        "verified": False,
        "method": "ML Prediction",
        "matches": [],
        "prediction": prediction
    }


if __name__ == "__main__":

    query = input("Enter news or URL:\n")

    result = verify_news(query)

    print()
    print(json.dumps(result, indent=4, ensure_ascii=False))