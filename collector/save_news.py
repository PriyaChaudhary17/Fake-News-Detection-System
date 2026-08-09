import json
from pathlib import Path


def save_articles(source, articles):
    """
    Save articles from one source into a JSON file.
    """

    folder = Path("data/raw/rss")
    folder.mkdir(parents=True, exist_ok=True)

    filename = folder / f"{source.lower().replace(' ', '_')}.json"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(articles, file, ensure_ascii=False, indent=4)

    print(f"Saved {len(articles)} articles to {filename}")