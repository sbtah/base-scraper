import time
from random import randint
from typing import List, Union

from lxml.html import HtmlElement, HTMLParser, fromstring
from scraper.helpers.logger import logger
from scraper.logic.base import BaseScraper
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotVisibleException,
    NoSuchElementException,
)
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager


class BaseSeleniumScraper(BaseScraper):
    """
    Base selenium scraper class with logic related to requesting and processing webpages.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._driver = None
        self.teardown = True

    def __str__(self) -> str:
        return f'Scraper: {self.desired_url}'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.driver.delete_all_cookies()
            self.driver.quit()

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    @property
    def element(self) -> HtmlElement:
        """
        Parse page source and return HtmlElement.
        """
        hp = HTMLParser(encoding="utf-8")
        html_element = fromstring(self.driver.page_source, parser=hp)
        return html_element

    def wait(self, seconds: int) -> None:
        """
        Custom wait function that sleeps for specified amount of seconds.
        While waiting method also pings driver each second.
        """
        for _ in range(1, seconds + 1):
            self.logger.debug(f'Waiting for: {_}/{seconds} seconds, at url: {self.current_url}')
            time.sleep(1)

    def random_sleep_small(self) -> None:
        """Custom sleep function that sleeps from 1 to 3 seconds"""
        value = randint(1, 3)
        logger.debug(f'Small sleep for: {value} seconds.')
        return self.wait(value)

    def random_sleep_medium(self) -> None:
        """Custom sleep function that sleeps from 3 to 6 seconds"""
        value = randint(3, 6)
        logger.debug(f'Medium sleep for: {value} seconds.')
        return self.wait(value)

    def random_sleep_long(self) -> None:
        """Custom sleep function that sleeps from 6 to 8 seconds"""
        value = randint(6, 8)
        logger.debug(f'Long sleep for: {value} seconds.')
        return self.wait(value)

    def random_sleep_deep(self) -> None:
        """Custom sleep function that sleeps from 15 to 20 seconds"""
        value = randint(15, 20)
        logger.debug(f'Deep sleep for: {value} seconds')
        return self.wait(value)

    @property
    def driver(self) -> webdriver:

        if self._driver is None:
            options = webdriver.ChromeOptions()

            options.add_argument('--no-sandbox')
            options.add_argument('--single-process')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--incognito')
            options.add_argument('--disable-infobars')
            options.add_argument('--ignore-ssl-errors=yes')
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--start-maximized')

            # TODO:
            # Call get_random_proxy to use different proxy server on each request..
            if self.proxy is not None:
                options.add_argument(f'--proxy-server={self.proxy}')
            # self.options.add_argument('--proxy-server=socks5://127.0.0.1:9050')

            # User Agent
            options.add_argument(f'--user-agent={self.random_user_agent}')

            # Bypass Bot detection
            options.add_experimental_option(
                'excludeSwitches', ['enable-automation'],
            )
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument(
                '--disable-blink-features=AutomationControlled'
            )

            # Remote
            # self._driver = webdriver.Remote(
            #     command_executor='http://comp-chrome:4444/wd/hub',
            #     options=options,
            #     desired_capabilities=DesiredCapabilities.CHROME,
            # )

            # Locally installed browser just for testing.
            self._driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options,
            )

            self._driver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
            screen_size = self.random_screen_resolution
            self._driver.set_window_size(screen_size[0], screen_size[1])

        return self._driver

    def request(self) -> bool:
        """
        Request specified url.
        """
        try:
            self.driver.get(self.desired_url)
            self.logger.info(f"Requesting url: {self.desired_url}")
            self.random_sleep_small()
            return True
        except Exception as e:
            self.logger.error(f"(request) Exception: {e}")
            return False
