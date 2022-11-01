from scraper.logic.base import BaseScraper
import time

if __name__ == "__main__":
    with BaseScraper() as scraper:
        response = scraper.selenium_get("https://www.castorama.pl/")
        element = scraper.parse_response(response)
        time.sleep(10)
        button = scraper.find_selenium_element('//button[@name="Wybierz sklep"]')
        scraper.initialize_html_element(
            selenium_element=button,
        )
