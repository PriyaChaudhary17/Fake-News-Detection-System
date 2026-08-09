import requests
from bs4 import BeautifulSoup


def scrape_article(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=15)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "lxml")

    # -------------------------
    # Title
    # -------------------------
    title = soup.find(class_="single-title")

    title = title.get_text(strip=True) if title else ""

    # -------------------------
    # Article Body
    # -------------------------
    article = soup.find(class_="post-entry")

    if not article:
        return None

    paragraphs = article.find_all("p")

    content = []

    for p in paragraphs:

        text = p.get_text(" ", strip=True)

        if len(text) > 20:
            content.append(text)

    return {
        "title": title,
        "content": "\n".join(content),
        "url": url,
        "source": "RONB"
    }


if __name__ == "__main__":

    url = "https://www.ronbpost.com/2026/07/17924/"

    article = scrape_article(url)

    print(article["title"])
    print()
    print(article["content"])