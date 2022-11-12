from scraper.sites.kiddymoon import KiddyMoon
from scraper.sites.castorama import Castorama
import time
from urllib.parse import urljoin
from lxml.html import tostring


products_url_kiddy = "https://kiddymoon.pl/pl/menu/pilki-do-basenu-1466.html"
products_url_casto = (
    "https://www.castorama.pl/produkty/urzadzanie/zarowki-i-swietlowki/zarowki-led.html"
)

if __name__ == "__main__":
    with KiddyMoon() as scraper:

        response = scraper.selenium_get(products_url_kiddy)
        products = scraper.find_products_for_all_pages()
        for prod in products:
            prod
        ### GET ELEMENT WITH SELENIUM
        # response = scraper.selenium_get(scraper.main_url)
        # element = scraper.parse_response(response=response)
        # categories_to_track = scraper.extract_urls_with_names_selenium(
        #     xpath_to_search=scraper.main_categories_xpath,
        #     url_name_attr="title",
        # )
        # for cat in categories_to_track:
        #     print(cat)

        ### GET ELEMENT WITH PYTHON
        # response = scraper.selenium_get(scraper.main_url)
        # element = scraper.parse_response(response=response)
        # categories_to_track = scraper.find_all_elements(
        #     html_element=element,
        #     xpath_to_search=scraper.main_categories_xpath,
        #     # name_xpath="./@title",
        # )
        # print(categories_to_track)
        # for cat in categories_to_track:
        #     print(cat.xpath("./@href")[0])
        # response_python = scraper.python_get(scraper.main_url)
        # with open(f"response-python.txt", "w") as f:
        #     f.write(response_python)
        # python_el = scraper.parse_response(response_python)
        # with open(f"element-python.txt", "w") as f:
        #     elem = tostring(python_el)
        #     f.write(str(elem))

        # response_selenium = scraper.selenium_get(scraper.main_url)
        # with open(f"response-selenium.txt", "w") as f:
        #     f.write(response_selenium)
        # selenium_el = scraper.parse_response(response_selenium)
        # with open(f"element-selenium.txt", "w") as f:
        #     elem = tostring(selenium_el)
        #     f.write(str(elem))
