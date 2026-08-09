import json
import os
from datetime import datetime

RSS_FOLDER = "dataset/raw/rss"
OUTPUT_FILE = "dataset/verified_news.json"

FILES = {
    "bbc_nepali.json": "BBC Nepali",
    "onlinekhabar.json": "Onlinekhabar",
    "nepal_press.json": "Nepal Press",
    "ronb.json": "RONB",
}

MIN_CONTENT_LENGTH = 100


def load_json(path):
    if not os.path.exists(path):
        print(f"Missing: {path}")
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {path}: {e}")
        return []

    if not isinstance(data, list):
        print(f"Unexpected format in {path} (expected a list), skipping")
        return []

    return data


def main():
    all_articles = []
    seen = set()

    for filename, source in FILES.items():
        filepath = os.path.join(RSS_FOLDER, filename)
        articles = load_json(filepath)
        print(f"{filename}: {len(articles)} articles loaded")

        added = 0
        skipped_empty = 0
        skipped_thin = 0
        skipped_dupe = 0

        for article in articles:
            if not isinstance(article, dict):
                continue

            title = (article.get("title") or "").strip()
            content = (article.get("content") or "").strip()
            url = (article.get("url") or "").strip()
            published = (article.get("published") or "").strip()

            if not title:
                skipped_empty += 1
                continue

            if len(content) < MIN_CONTENT_LENGTH:
                skipped_thin += 1
                continue

            # Prefer URL as the dedup key since it's a more reliable unique
            # identifier than title; fall back to title if URL is missing.
            key = url if url else title.lower()
            if key in seen:
                skipped_dupe += 1
                continue
            seen.add(key)

            all_articles.append({
                "title": title,
                "content": content,
                "url": url,
                "published": published,
                "source": source,
                "collected_at": datetime.now().isoformat()
            })
            added += 1

        print(
            f"  -> {added} kept, {skipped_dupe} duplicates, "
            f"{skipped_thin} thin content, {skipped_empty} missing title"
        )

    if not all_articles:
        print("\nNo articles collected from any source, aborting save "
              "to avoid overwriting existing output.")
        return

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    all_articles.sort(
    key=lambda x: x.get("published", ""),
    reverse=True
)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=4)

    print("\n======================================")
    print(f"Saved {len(all_articles)} unique articles")
    print(f"Database created: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
