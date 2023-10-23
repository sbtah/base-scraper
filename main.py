from scraper.logic.selenium import BaseSeleniumScraper
import time


if __name__ == "__main__":
    with BaseSeleniumScraper(desired_url='http://google.com') as scraper:
        scraper.request()
        print(scraper.time_started)




