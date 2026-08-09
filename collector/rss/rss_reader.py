import feedparser

from config.rss_feeds import RSS_FEEDS
from collector.save_news import save_articles
from collector.scraper_manager import scrape


# =====================================================
# Fetch one RSS feed
# =====================================================

def fetch_feed(source, rss_url):

    feed = feedparser.parse(rss_url)

    articles = []

    print(f"\nFetching {source}...")
    print(f"Found {len(feed.entries)} articles")

    for entry in feed.entries:

        print(f"Scraping: {entry.link}")

        article = scrape(entry.link)

        if article:

            article["source"] = source
            article["url"] = entry.link
            article["published"] = entry.get("published", "")

            articles.append(article)

    return articles


# =====================================================
# Fetch ALL latest articles
# =====================================================

def fetch_all_articles():

    all_articles = []

    for source, rss_url in RSS_FEEDS.items():

        try:

            articles = fetch_feed(source, rss_url)

            all_articles.extend(articles)

        except Exception as e:

            print(f"Failed to fetch {source}: {e}")

    print(f"\nTotal live articles: {len(all_articles)}")

    return all_articles


# =====================================================
# Save articles to database (Collector Mode)
# =====================================================

def collect_and_save():

    for source, rss_url in RSS_FEEDS.items():

        print("\n" + "=" * 60)
        print(source)
        print("=" * 60)

        articles = fetch_feed(source, rss_url)

        save_articles(source, articles)

        print(f"Saved {len(articles)} articles.")


# =====================================================
# Test
# =====================================================

if __name__ == "__main__":

    collect_and_save()