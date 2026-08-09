import requests
from bs4 import BeautifulSoup

SOURCE = "NEB News"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )
}


def scrape(url):

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Save HTML for inspection
    with open("nebnews.html", "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    print("HTML saved as nebnews.html")

    # ==========================================
    # Title
    # ==========================================

    title = ""

    for selector in [
        "h1.entry-title",
        "h1.post-title",
        "h1"
    ]:

        tag = soup.select_one(selector)

        if tag:
            title = tag.get_text(" ", strip=True)
            if title:
                break

    # ==========================================
    # Published Date
    # ==========================================

    published = ""

    for selector in [
        "time",
        ".entry-date",
        ".post-date",
        ".published"
    ]:

        tag = soup.select_one(selector)

        if tag:
            published = tag.get_text(" ", strip=True)
            if published:
                break

    # ==========================================
    # Content
    # ==========================================

    content = ""

    selectors = [
        "div.entry-content",
        "div.td-post-content",
        "div.post-content",
        "article .entry-content",
        "article"
    ]

    for selector in selectors:

        container = soup.select_one(selector)

        if not container:
            continue

        for bad in container.select(
            "script,style,iframe,figure,aside,form,noscript"
        ):
            bad.decompose()

        paragraphs = []

        for p in container.find_all(["p", "li", "h2", "h3"]):

            txt = p.get_text(" ", strip=True)

            if txt:
                paragraphs.append(txt)

        if paragraphs:
            content = "\n\n".join(paragraphs)
            break

    if not content:

        body = soup.find("body")

        if body:
            content = body.get_text("\n", strip=True)

    return {
        "title": title,
        "content": content,
        "url": url,
        "published": published,
        "source": SOURCE
    }


if __name__ == "__main__":

    url = input("Enter NEB News URL:\n")

    article = scrape(url)

    print("\n" + "=" * 80)

    print("\nTITLE")
    print("-" * 40)
    print(article["title"])

    print("\nCONTENT")
    print("-" * 40)
    print(article["content"])

    print("\nURL")
    print("-" * 40)
    print(article["url"])

    print("\nPUBLISHED")
    print("-" * 40)
    print(article["published"])

    print("\nSOURCE")
    print("-" * 40)
    print(article["source"])