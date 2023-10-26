import time
from random import choice
from typing import List

from scraper.helpers.logger import logger
from scraper.options.settings import RESOLUTIONS, USER_AGENTS


class BaseScraper:
    """
    Base scraper class.
    """
    def __init__(self, desired_url: str, proxy=None):
        self.desired_url = desired_url
        self.proxy = proxy
        self.logger = logger
        self.time_started = time.time()

    @property
    def random_user_agent(self) -> str:
        """
        Return str with random User-Agent.
        """
        agent = choice(USER_AGENTS)
        return agent

    @property
    def random_screen_resolution(self) -> List[str]:
        """
        Return list with screen resolution size.
        """
        screen_params = choice(RESOLUTIONS)
        return screen_params




