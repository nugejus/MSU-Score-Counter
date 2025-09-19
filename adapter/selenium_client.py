# adapters/selenium_client.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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

    def current_url(self) -> str:
        return self.driver.current_url

    def exists(self, by: str, selector: str, timeout: float = 0) -> bool:
        """요소 존재 여부. timeout>0이면 대기 후 판정."""
        by_map = {"name": By.NAME, "css": By.CSS_SELECTOR, "link": By.LINK_TEXT, "xpath": By.XPATH}
        try:
            if timeout > 0:
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((by_map[by], selector))
                )
                return True
            else:
                self.driver.find_element(by_map[by], selector)
                return True
        except Exception:
            return False

    def wait_visible(self, by: str, selector: str, timeout: float = 5) -> bool:
        """지정 요소가 보일 때까지 대기. 보이면 True, 타임아웃이면 False."""
        by_map = {"name": By.NAME, "css": By.CSS_SELECTOR, "link": By.LINK_TEXT, "xpath": By.XPATH}
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by_map[by], selector))
            )
            return True
        except TimeoutException:
            return False

    def text(self, by: str, selector: str) -> str:
        by_map = {"name": By.NAME, "css": By.CSS_SELECTOR, "link": By.LINK_TEXT, "xpath": By.XPATH}
        try:
            return self.driver.find_element(by_map[by], selector).text.strip()
        except Exception:
            return ""