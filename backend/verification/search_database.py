import json
import os
import re

DATABASE = "dataset/verified_news.json"

# Minimum fraction of query words that must appear in an article's content
# for it to count as a content match. Substring matching alone is too
# strict for full scraped article bodies (whitespace/punctuation differences
# almost always break an exact "query in value" check).
CONTENT_MATCH_THRESHOLD = 0.6

# Ignore very short/common words when doing token-overlap matching so a
# handful of stopwords can't inflate the match ratio.
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "is", "are", "was", "were",
    "of", "in", "on", "at", "to", "for", "with", "as", "by", "that",
    "this", "it", "from", "be", "has", "have", "had"
}


def load_database():

    print("\nLoading database from:")
    print(os.path.abspath(DATABASE))

    if not os.path.exists(DATABASE):
        raise FileNotFoundError(
            f"{DATABASE} not found."
        )

    with open(DATABASE, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Articles loaded:", len(data))

    return data


def _normalize(value):
    """Coerce a field value to a clean, lowercase string.

    Guards against non-string field values (e.g. a malformed JSON entry
    where 'title' or 'content' ended up as a list or number) and collapses
    whitespace/punctuation so near-identical strings compare equal.
    """
    if value is None:
        return ""
    if not isinstance(value, str):
        value = str(value)
    value = value.lower()
    value = re.sub(r"[^\w\s]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def search(database, query, field):
    """Search a list of articles for `query` as a substring of the given field."""
    query = _normalize(query)
    results = []
    for article in database:
        value = _normalize(article.get(field))
        if query and query in value:
            results.append(article)
    return results


def search_by_title(database, query):
    return search(database, query, "title")


def search_by_content(database, query):
    """Match articles whose content shares enough vocabulary with the query.

    Plain substring matching doesn't work well here: `query` is often a
    full scraped article body, and even trivial whitespace/formatting
    differences from the source page will break an exact 'in' check.
    Instead, this checks what fraction of the query's significant words
    appear in each article's content, and keeps articles above
    CONTENT_MATCH_THRESHOLD, ranked by overlap (best match first).
    """
    query_words = {
        w for w in _normalize(query).split() if w not in STOPWORDS and len(w) > 2
    }

    if not query_words:
        return []

    scored = []
    for article in database:
        content_words = set(_normalize(article.get("content")).split())
        if not content_words:
            continue
        overlap = len(query_words & content_words) / len(query_words)
        if overlap >= CONTENT_MATCH_THRESHOLD:
            scored.append((overlap, article))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [article for _, article in scored]


def print_results(results, limit=5):
    for article in results[:limit]:
        print("-" * 60)
        print("Source :", article.get("source", "N/A"))
        print("Title  :", article.get("title", "N/A"))
        print("URL    :", article.get("url", "N/A"))


def main():
    try:
        database = load_database()
    except FileNotFoundError as e:
        print(e)
        return

    query = input("Enter search text: ").strip()
    if not query:
        print("Please enter a search term.")
        return

    print("\nSearching title...")
    title_results = search_by_title(database, query)
    print(f"Found {len(title_results)} matches")
    print_results(title_results)

    print("\nSearching content...")
    content_results = search_by_content(database, query)
    print(f"Found {len(content_results)} matches")
    print_results(content_results)


if __name__ == "__main__":
    main()