from scraper.logic.base import BaseScraper
import time

if __name__ == "__main__":
    with BaseScraper() as scraper:
        response = scraper.python_get("https://meowbaby.eu/")
        elem = scraper.parse_response(response)
