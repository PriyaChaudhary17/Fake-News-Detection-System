from collector.scraper_manager import scrape

url = "https://www.onlinekhabar.com/2026/07/1973775/these-are-the-four-greats-who-reached-the-semi-finals-of-the-fifa-world-cup"

article = scrape(url)

print(article["title"])
print(article["source"])
print(len(article["content"]))