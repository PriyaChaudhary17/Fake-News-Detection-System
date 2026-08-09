import feedparser


RSS_FEEDS = {
    "BBC Nepali": "https://feeds.bbci.co.uk/nepali/rss.xml",
    "Onlinekhabar": "https://www.onlinekhabar.com/feed",
    "Nepal Press": "https://nepalpress.com/feed"
}


def fetch_latest_articles():

    articles = []

    for source, url in RSS_FEEDS.items():

        print(f"Fetching {source}...")

        feed = feedparser.parse(url)

        for entry in feed.entries:

            articles.append({
                "source": source,
                "title": entry.get("title", ""),
                "url": entry.get("link", ""),
                "published": entry.get("published", "")
            })

    return articles


if __name__ == "__main__":

    articles = fetch_latest_articles()

    print(f"\nTotal Articles: {len(articles)}\n")

    for article in articles[:10]:
        print(article["source"])
        print(article["title"])
        print(article["url"])
        print()