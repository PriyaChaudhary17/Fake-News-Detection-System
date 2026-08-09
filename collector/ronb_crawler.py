import re
import time
import logging
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

from collector.scrapers.ronb import scrape_article
from collector.save_news import save_articles

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)

BASE_URL = "https://www.ronbpost.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# Matches article URLs like:
# https://www.ronbpost.com/2026/07/17924/
DATE_PATH_RE = re.compile(r"/\d{4}/\d{2}/")

REQUEST_DELAY = 1.0


# ---------------------------------------------------
# Utility Functions
# ---------------------------------------------------

def normalize_url(url):
    """
    Remove query parameters and fragments.
    """

    parsed = urlparse(url)

    return urlunparse(
        parsed._replace(
            query="",
            fragment=""
        )
    )


# ---------------------------------------------------
# Collect Latest Article Links
# ---------------------------------------------------

def get_latest_links():

    try:

        response = requests.get(
            BASE_URL,
            headers=HEADERS,
            timeout=15
        )

    except requests.RequestException as e:

        logger.error(f"Failed to access RONB: {e}")
        return []

    if response.status_code != 200:

        logger.error(f"HTTP {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "lxml")

    links = set()

    for a in soup.find_all("a", href=True):

        href = a["href"]

        full_url = urljoin(BASE_URL, href)

        parsed = urlparse(full_url)

        # Ignore external links
        if "ronbpost.com" not in parsed.netloc:
            continue

        # Keep only article URLs
        if not DATE_PATH_RE.search(parsed.path):
            continue

        links.add(normalize_url(full_url))

    return sorted(links, reverse=True)


# ---------------------------------------------------
# Main
# ---------------------------------------------------

def main():

    urls = get_latest_links()

    logger.info(f"Found {len(urls)} article URLs")

    if not urls:
        logger.warning("No article URLs found.")
        return

    articles = []

    for i, url in enumerate(urls, start=1):

        logger.info(f"[{i}/{len(urls)}] Scraping: {url}")

        try:

            article = scrape_article(url)

            if (
                article
                and article["title"].strip()
                and len(article["content"].strip()) > 100
            ):

                articles.append(article)

        except Exception as e:

            logger.warning(f"Error scraping {url}")
            logger.warning(e)

        if i < len(urls):
            time.sleep(REQUEST_DELAY)

    if articles:

        save_articles("ronb", articles)

    else:

        logger.warning("No valid articles collected.")

    logger.info("=" * 50)
    logger.info(f"Collected {len(articles)} articles")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()