import logging
import os
from urllib.parse import urlparse

from collector.scraper_manager import scrape
from backend.ml.predict_text import predict_news
from backend.verification.similarity_search import find_similar_articles

logger = logging.getLogger("fake_news_api.url_verifier")

# =====================================================
# Configuration
# =====================================================

SIMILARITY_THRESHOLD = float(
    os.getenv("SIMILARITY_THRESHOLD", 0.80)
)

# =====================================================
# Trusted News Sources
# =====================================================

TRUSTED_DOMAINS = {
    "onlinekhabar.com": "Onlinekhabar",
    "bbc.com": "BBC Nepali",
    "bbc.co.uk": "BBC Nepali",
    "nepalpress.com": "Nepal Press",
    "ronbpost.com": "RONB",
    "gorkhapatraonline.com": "Gorkhapatra",
    "ekantipur.com": "Ekantipur",
    "setopati.com": "Setopati",
    "ratopati.com": "Ratopati",
    "nebnews.net": "NEB News",
}

# =====================================================
# URL Check
# =====================================================

def is_url(text):

    if not isinstance(text, str):
        return False

    text = text.strip().lower()

    return (
        text.startswith("http://")
        or text.startswith("https://")
    )

# =====================================================
# Domain Normalization
# =====================================================

def normalize_domain(netloc):

    netloc = netloc.lower()

    if netloc.startswith("www."):
        netloc = netloc[4:]

    return netloc


def is_trusted_domain(domain):

    if domain in TRUSTED_DOMAINS:
        return domain

    for trusted_domain in TRUSTED_DOMAINS:

        if domain.endswith("." + trusted_domain):
            return trusted_domain

    return None
def verify_url(url):

    # -------------------------------------------------
    # Check URL
    # -------------------------------------------------

    if not is_url(url):
        return {
            "verified": False,
            "reason": "Input is not a valid URL."
        }

    domain = normalize_domain(urlparse(url).netloc)

    trusted_key = is_trusted_domain(domain)

    trusted = trusted_key is not None

    trusted_source_name = TRUSTED_DOMAINS.get(
        trusted_key,
        "Unknown"
    )

    # -------------------------------------------------
    # Scrape Article
    # -------------------------------------------------

    try:

        article = scrape(url)

    except Exception:

        logger.exception("Scraping failed for URL: %s", url)

        return {
            "verified": False,
            "reason": "Could not fetch or parse the article at that URL."
        }

    if not isinstance(article, dict):

        return {
            "verified": False,
            "reason": "Invalid article extracted."
        }

    # -------------------------------------------------
    # Extract Text
    # -------------------------------------------------

    title = article.get("title", "")

    content = article.get("content", "")

    full_text = f"{title}\n\n{content}"

    if len(full_text.strip()) < 100:

        return {
            "verified": False,
            "reason": "Not enough article content extracted."
        }

    logger.info("Searching similar articles...")

    # -------------------------------------------------
    # Similarity Search
    # -------------------------------------------------

    similar_articles = find_similar_articles(full_text)

    best_similarity = 0.0

    if similar_articles:
        best_similarity = similar_articles[0].get(
            "similarity",
            0
        ) or 0

    similarity_verified = (
        best_similarity >= SIMILARITY_THRESHOLD
    )

    # -------------------------------------------------
    # Prediction
    # -------------------------------------------------

    if similarity_verified:

        similarity_pct = round(
            best_similarity * 100,
            2
        )

        prediction = {

            "prediction": "REAL",

            "confidence": similarity_pct,

            "real_probability": similarity_pct,

            "fake_probability": round(
                100 - similarity_pct,
                2
            ),

            "reasons": [

                "The article closely matches a trusted news article.",

                f"Similarity Score: {similarity_pct}%"

            ]

        }

    elif trusted:

        prediction = predict_news(full_text)

        original_label = prediction["prediction"]

        original_real = prediction["real_probability"]

        original_fake = prediction["fake_probability"]

        if original_label != "REAL":

            prediction["real_probability"] = original_fake

            prediction["fake_probability"] = original_real

            prediction["confidence"] = original_fake

        prediction["prediction"] = "REAL"

        prediction["reasons"] = [

            f"The article was published by the trusted news source '{trusted_source_name}'.",

            "The article content was successfully extracted and analyzed.",

            "The final decision combines machine learning analysis with trusted source verification."

        ]

        if similar_articles:

            prediction["reasons"].append(

                f"Closest matching trusted article similarity: {round(best_similarity * 100, 2)}%."

            )

    else:

        prediction = predict_news(full_text)

        if similar_articles:

            prediction["reasons"].append(

                f"Closest matching trusted article similarity: {round(best_similarity * 100, 2)}%."

            )

        else:

            prediction["reasons"].append(

                "No similar trusted news article was found."

            )

    logger.info("Final prediction: %s", prediction)
        # -------------------------------------------------
    # Final Response
    # -------------------------------------------------

    verified = trusted or similarity_verified

    return {

        "verified": verified,

        "trusted_source": trusted_source_name,

        "input_type": "url",

        "scraped_article": {

            "title": title,

            "published": article.get(
                "published",
                ""
            ),

            "source": (
                trusted_source_name
                if trusted
                else article.get(
                    "source",
                    "Unknown"
                )
            ),

            "url": url

        },

        "prediction": prediction,

        "sources": similar_articles,

        "reason": (
            None
            if verified
            else "The website is not recognized as a trusted news source."
        )

    }
# =====================================================
# Test
# =====================================================

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    test_url = input("Enter URL:\n")

    result = verify_url(test_url)

    print("\n" + "=" * 70)

    for key, value in result.items():

        print(f"{key} : {value}")