from scraper.logic.base import BaseScraper

if __name__ == "__main__":
    with BaseScraper() as scraper:
        response = scraper.python_get("https://meowbaby.eu/")
        print(response)
