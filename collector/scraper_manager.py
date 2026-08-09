from collector.scrapers.onlinekhabar import scrape_article as scrape_onlinekhabar
from collector.scrapers.bbc_nepali import scrape_article as scrape_bbc
from collector.scrapers.nepalpress import scrape_article as scrape_nepalpress
from collector.scrapers.ronb import scrape_article as scrape_ronb

from collector.scrapers.generic_scraper import scrape_article as scrape_generic


def scrape(url):

    if "onlinekhabar.com" in url:
        return scrape_onlinekhabar(url)

    elif "bbc.com" in url:
        return scrape_bbc(url)

    elif "nepalpress.com" in url:
        return scrape_nepalpress(url)

    elif "ronbpost.com" in url:
        return scrape_ronb(url)

    else:
        # Any other news website
        return scrape_generic(url)