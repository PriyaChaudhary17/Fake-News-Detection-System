import json
import requests
import trafilatura

from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# =====================================================
# Create HTTP Session
# =====================================================

def _make_session():

    session = requests.Session()

    retries = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    session.mount("https://", HTTPAdapter(max_retries=retries))
    session.mount("http://", HTTPAdapter(max_retries=retries))

    return session


# =====================================================
# Scrape Single Article
# =====================================================

def scrape_article(url):

    session = _make_session()

    try:

        response = session.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            allow_redirects=True
        )

        response.raise_for_status()

    except Exception as e:

        raise Exception(f"Unable to download webpage: {e}")

    html = response.content

    extracted = trafilatura.extract(
        html,
        url=url,
        include_comments=False,
        include_tables=False,
        include_links=False,
        output_format="json"
    )

    if extracted is None:
        raise Exception("Could not extract article.")

    try:
        article = json.loads(extracted)

    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse extracted content: {e}")

    # -------------------------------------
    # Title fallback
    # -------------------------------------

    title = (article.get("title") or "").strip()

    if not title:

        soup = BeautifulSoup(html, "html.parser")

        if soup.title:
            title = soup.title.get_text(strip=True)

        elif soup.find("h1"):
            title = soup.find("h1").get_text(strip=True)

    content = (article.get("text") or "").strip()

    return {

        "title": title,
        "content": content,
        "url": url,
        "published": article.get("date", "")

    }


# =====================================================
# Scrape Multiple Articles
# =====================================================

def scrape_articles(article_list):

    scraped_articles = []

    total = len(article_list)

    print(f"\nScraping {total} articles...\n")

    for index, article in enumerate(article_list, start=1):

        print(f"[{index}/{total}] {article['source']}")

        try:

            scraped = scrape_article(article["url"])

            scraped_articles.append({

                "source": article["source"],
                "title": scraped["title"],
                "content": scraped["content"],
                "url": scraped["url"],
                "published": scraped["published"]

            })

        except Exception as e:

            print(f"Failed: {article['url']}")
            print(e)

    print(f"\nSuccessfully scraped {len(scraped_articles)} articles.\n")

    return scraped_articles


# =====================================================
# Test
# =====================================================

if __name__ == "__main__":

    from collector.rss.rss_reader import fetch_latest_articles

    latest_articles = fetch_latest_articles()

    scraped_articles = scrape_articles(latest_articles)

    print("=" * 70)

    if scraped_articles:

        article = scraped_articles[0]

        print("Source:")
        print(article["source"])

        print("\nTitle:")
        print(article["title"])

        print("\nURL:")
        print(article["url"])

        print("\nPublished:")
        print(article["published"])

        print("\nContent:")
        print(article["content"][:1000])