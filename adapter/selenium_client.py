# adapters/selenium_client.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from ports import WebClientPort
import time

class SeleniumClient(WebClientPort):
    def __init__(self):
        opts = webdriver.ChromeOptions()
        opts.add_argument("--headless")
        self.driver = webdriver.Chrome(options=opts)

    def open(self, url: str) -> None:
        self.driver.get(url)

    def wait(self, seconds: float) -> None:
        time.sleep(seconds)

    def find_and_type(self, by: str, selector: str, text: str, paste: bool=False) -> None:
        by_map = {"name": By.NAME, "css": By.CSS_SELECTOR, "link": By.LINK_TEXT}
        el = self.driver.find_element(by_map[by], selector)
        el.click()
        el.clear()
        el.send_keys(text)

    def click(self, by: str, selector: str) -> None:
        by_map = {"name": By.NAME, "css": By.CSS_SELECTOR, "link": By.LINK_TEXT}
        self.driver.find_element(by_map[by], selector).click()

    def page_source(self) -> str:
        return self.driver.page_source

    def close(self) -> None:
        self.driver.quit()
