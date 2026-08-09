import json
import re
import unicodedata
import os

INPUT = "dataset/processed/real_news.json"
OUTPUT = "dataset/processed/clean_real_news.json"


def clean(text):
    if not text:
        return ""

    # Normalize Unicode
    text = unicodedata.normalize("NFC", text)

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Remove zero-width characters
    text = text.replace("\u200b", "")
    text = text.replace("\ufeff", "")

    return text.strip()


with open(INPUT, "r", encoding="utf-8") as f:
    articles = json.load(f)

clean_articles = []

for article in articles:

    title = clean(article.get("title", ""))
    content = clean(article.get("content", ""))

    # Skip articles with little content
    if len(content) < 100:
        continue

    article["title"] = title
    article["content"] = content

    clean_articles.append(article)

os.makedirs("dataset/processed", exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(clean_articles, f, ensure_ascii=False, indent=4)

print("=" * 50)
print(f"Original articles : {len(articles)}")
print(f"Clean articles    : {len(clean_articles)}")
print(f"Saved to          : {OUTPUT}")