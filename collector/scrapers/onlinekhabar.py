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

    # Title
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else ""

    # Body
    article_div = soup.find("div", class_="ok18-single-post-content-wrap")

    paragraphs = []

    if article_div:
        for p in article_div.find_all("p"):
            text = p.get_text(strip=True)

            if text:
                paragraphs.append(text)

    article = {
        "title": title,
        "content": "\n".join(paragraphs),
        "url": url,
        "source": "Onlinekhabar"
    }

    return article


if __name__ == "__main__":

    url = "https://www.onlinekhabar.com/2026/07/1973775/these-are-the-four-greats-who-reached-the-semi-finals-of-the-fifa-world-cup"

    article = scrape_article(url)

    print(article)