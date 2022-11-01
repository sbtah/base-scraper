import asyncio
import httpx

from lxml.html import HtmlElement, HTMLParser, fromstring
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.common.exceptions import (
    ElementNotVisibleException,
    NoSuchElementException,
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from scraper.helpers.logging import logging
from scraper.helpers.randoms import random_sleep_small


class BaseScraper:
    """"""

    def __init__(self, *args, **kwargs):
        self._driver = None
        self.teardown = True

    def __str__(self):
        return "Base Scraper"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.driver.quit()

    def get_random_user_agent(self):
        pass

    def get_random_proxy(self):
        pass

    @property
    def user_agent(self):
        return "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"

    @property
    def driver(self):

        if self._driver is None:
            options = webdriver.ChromeOptions()
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            # TODO:
            # Call get_random_user_agent to use different User-Agent server on each request..
            options.add_argument(self.user_agent)
            options.add_argument("--no-sandbox")
            options.add_argument("--start-maximized")
            options.add_argument("--single-process")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--incognito")
            # TODO:
            # Call get_random_proxy to use different proxy server on each request..
            # self.options.add_argument('--proxy-server=176.9.220.108:8080')
            # self.options.add_argument("--headless")
            options.add_argument("--disable-blink-features")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-infobars")
            options.add_argument("--ignore-ssl-errors=yes")
            options.add_argument("--ignore-certificate-errors")
            options.add_experimental_option("useAutomationExtension", False)
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            self._driver = webdriver.Remote(
                command_executor="http://localhost:4444",
                desired_capabilities=DesiredCapabilities.CHROME,
                options=options,
            )

        return self._driver

    def selenium_get(self, url):
        """
        Requests specified url.
        :param url: Requested URL.
        Returns driver's page_source.
        """

        assert url, "Request failed, No proper url for GET."

        try:
            self.driver.get(url)
            logging.info(f"Requesting: {url}")
            random_sleep_small()
            return self.driver.page_source
        except Exception as e:
            logging.error(f"(selenium_get) Exception: {e}")
            return None

    def python_get(self, url):
        """
        Request specifed url.
        :param url: Requested URL.
        Return's text response.
        """

        # TODO:
        # User-Agent Rotation
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        }

        assert url, "Request failed, No proper url for GET."

        try:
            response = httpx.get(url, timeout=30, headers=headers)
            logging.info(f"Requesting: {url}")
            random_sleep_small()
            response.raise_for_status()
            return response.text
        except httpx.TimeoutException:
            logging.error("Connection was timed out.")
            return None
        except httpx.ConnectError:
            logging.error("Connection Error.")
            return None
        except httpx.HTTPError:
            logging.error("HTTPError was raised.")
            return None
        except Exception as e:
            logging.error(f"(python_get) Exception: {e}")

    async def async_get(self, session, url):
        """
        Request url with async.
        :param url: Requested URL.
        :param session: Session is used while connecting.
        Return's text response.
        """
        response = await session.get(url)
        return response.text

    async def get_pages(self, session, urls_list):
        """ """
        tasks = []
        for url in urls_list:
            tasks.append(asyncio.create_task(self.async_get(session, url)))

        requested = await asyncio.gather(*tasks)
        return requested

    async def execute_async_get(self, urls_list):
        """ """
        async with httpx.AsyncClient() as session:
            data = await self.get_pages(session=session, urls_list=urls_list)
            return data

    def run_crawler_async(self, function):
        asyncio.run(function)

    def parse_response(self, response):
        """
        Parse text response from get.
        Returns HtmlElement.
        :param response: Text response from GET.
        """

        assert response, logging.error(
            "Parsing response failed, received invalid response object."
        )

        try:
            element = fromstring(response)
            logging.info("Parsing response to HtmlElement.")
            return element
        except Exception as e:
            logging.error(f"(parse_response) Exception: {e}")

    def refresh_current_session(self):
        """
        Delete all cookies and refresh browser while using Selenium Driver.
        """
        self.driver.delete_all_cookies()
        self.driver.refresh()
        logging.info("Browser refreshed, cookies deleted.")

    def close_driver(self):
        """
        Close current driver.
        """
        if self.driver:
            self.driver.close()

    def return_selenium_element(self, xpath_to_search):
        """
        Finds element by specified Xpath.
        Return Selenium element to interact with.
        """
        try:
            element = self.driver.find_element(
                By.XPATH,
                xpath_to_search,
            )
            return element
        except ElementNotVisibleException as e:
            logging.error(f"Selenium element not visible: {e}")
            return None
        except Exception as e:
            logging.error(f"Selenium element not visible: {e}")
            return None
