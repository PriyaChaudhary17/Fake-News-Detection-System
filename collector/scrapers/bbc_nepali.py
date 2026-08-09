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
    title = soup.find("h1")

    if not title:
        return None

    title = title.get_text(strip=True)

    # Content
    paragraphs = []

    for p in soup.find_all("p"):

        text = p.get_text(" ", strip=True)

        if len(text) < 20:
            continue

        if text.startswith("तस्बिर स्रोत"):
            continue

        if text.startswith("End of"):
            continue

        if "बीबीसी न्यूज नेपाली" in text:
            continue

        if "©" in text:
            continue

        if "तपाईंको उपकरणमा मिडिया प्लेब्याक" in text:
            continue

        paragraphs.append(text)

    content = "\n".join(paragraphs)

    return {
        "title": title,
        "content": content,
        "url": url,
        "source": "BBC Nepali"
    }


if __name__ == "__main__":

    url = "https://www.bbc.com/nepali/articles/c74yk22xx1do"

    article = scrape_article(url)

    print(article)