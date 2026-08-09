import requests
from bs4 import BeautifulSoup


def scrape_article(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        

        # ==================================================
        # TITLE
        # ==================================================

        title = ""

        title_tag = (
            soup.find("h1", class_="single-top-title mb-3 sticky-title")
            or soup.find("h1", class_="single-top-title")
            or soup.find("h1")
        )

        if title_tag:
            title = title_tag.get_text(" ", strip=True)

        # ==================================================
        # CONTENT
        # ==================================================

        content = ""

        article = (
            soup.find("div", class_="blog-details")
            or soup.find("div", class_="single-blog-content")
        )

        if article:

            paragraphs = article.find_all("p")

            texts = []

            for p in paragraphs:

                text = p.get_text(" ", strip=True)

                if len(text) > 20:
                    texts.append(text)

            content = "\n\n".join(texts)

        # ==================================================
        # PUBLISHED DATE
        # ==================================================

        published = ""

        for span in soup.find_all("span"):

            icon = span.find("i")

            if icon:

                classes = " ".join(icon.get("class", []))

                if "fa-calendar-alt" in classes:

                    published = span.get_text(" ", strip=True)

                    break

        # ==================================================
        # RESULT
        # ==================================================

        return {
            "title": title,
            "content": content,
            "published": published,
            "url": url,
            "source": "Gorkhapatra"
        }

    except Exception as e:

        print("Error:", e)

        return None


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    url = input("Enter Gorkhapatra URL:\n").strip()

    article = scrape_article(url)

    if article:

        print("\n" + "=" * 70)

        print("TITLE")
        print("-" * 70)
        print(article["title"])

        print("\nCONTENT")
        print("-" * 70)
        print(article["content"])

        print("\nPUBLISHED")
        print("-" * 70)
        print(article["published"])

        print("\nSOURCE")
        print("-" * 70)
        print(article["source"])

        print("\nURL")
        print("-" * 70)
        print(article["url"])

    else:

        print("Failed to scrape article.")