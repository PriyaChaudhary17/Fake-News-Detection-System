import requests
from bs4 import BeautifulSoup


def scrape_article(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "lxml")

        # Title
        title = soup.find("h1")
        title = title.get_text(strip=True) if title else ""

        # Try different containers
        article = (
            soup.find("div", class_="news-content-area")
            or soup.find("div", class_="news-post-content")
            or soup.find("div", class_="news-content")
            or soup.find("div", class_="post-detail")
        )

        if not article:
            print("Article body not found:", url)
            return None

        paragraphs = article.find_all("p")

        content = []

        for p in paragraphs:
            text = p.get_text(" ", strip=True)

            if len(text) > 40:
                content.append(text)

        if not content:
            print("No paragraphs found:", url)
            return None

        return {
            "title": title,
            "content": "\n".join(content),
            "url": url,
            "source": "Nepal Press"
        }

    except Exception as e:
        print("Error:", e)
        return None


if __name__ == "__main__":

    url = "https://nepalpress.com/2026/07/13/743551/congress-split-rehearsal-various-programs-on-bp-memorial-day"

    article = scrape_article(url)

    if article:
        print(article["title"])
        print()
        print(article["content"][:1000])