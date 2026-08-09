import json
import os

FILES = [
    "dataset/raw/rss/onlinekhabar.json",
    "dataset/raw/rss/bbc_nepali.json",
    "dataset/raw/rss/nepal_press.json",
    "dataset/raw/rss/ronb.json"
]

OUTPUT = "dataset/processed/real_news.json"

all_news = []
seen_urls = set()

for file in FILES:

    if not os.path.exists(file):
        print(f"Skipping: {file}")
        continue

    with open(file, "r", encoding="utf-8") as f:
        articles = json.load(f)

    print(f"Loaded {len(articles)} articles from {file}")

    for article in articles:

        url = article.get("url", "").strip()

        if url in seen_urls:
            continue

        seen_urls.add(url)

        all_news.append({
            "title": article.get("title", "").strip(),
            "content": article.get("content", "").strip(),
            "url": url,
            "source": article.get("source", "").strip(),
            "label": 0
        })

os.makedirs("dataset/processed", exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(all_news, f, ensure_ascii=False, indent=4)

print("\n" + "=" * 50)
print(f"Total Real News: {len(all_news)}")
print(f"Saved to: {OUTPUT}")