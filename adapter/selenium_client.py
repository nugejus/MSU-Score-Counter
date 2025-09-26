# adapters/selenium_client.py
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ports import WebClientPort


class SeleniumClient(WebClientPort):
    """Web client implementation using Selenium WebDriver (Chrome).

    This adapter implements the WebClientPort interface and provides
    methods to open pages, find elements, type values, click elements,
    and retrieve HTML source code.
    """

    def __init__(self):
        """Initialize the Selenium client with headless Chrome options."""
        opts = webdriver.ChromeOptions()
        opts.add_argument("--headless")
        self.driver = webdriver.Chrome(options=opts)

    def open(self, url: str) -> None:
        """Open a URL in the browser.

        Args:
            url (str): The URL to open.
        """
        self.driver.get(url)

    def wait(self, seconds: float) -> None:
        """Pause execution for a fixed amount of time.

        Args:
            seconds (float): Number of seconds to wait.
        """
        time.sleep(seconds)

    def find_and_type(
        self, by: str, selector: str, text: str, paste: bool = False
    ) -> None:
        """Find an element and type text into it.

        Args:
            by (str): Locator strategy ("name", "css", "link").
            selector (str): The selector string.
            text (str): The text to type into the element.
            paste (bool): Unused flag (reserved for clipboard-based typing).
        """
        by_map = {"name": By.NAME, "css": By.CSS_SELECTOR, "link": By.LINK_TEXT}
        el = self.driver.find_element(by_map[by], selector)
        el.click()
        el.clear()
        el.send_keys(text)

    def click(self, by: str, selector: str) -> None:
        """Find an element and perform a click action.

        Args:
            by (str): Locator strategy ("name", "css", "link").
            selector (str): The selector string.
        """
        by_map = {"name": By.NAME, "css": By.CSS_SELECTOR, "link": By.LINK_TEXT}
        self.driver.find_element(by_map[by], selector).click()

    def page_source(self) -> str:
        """Return the current page source.

        Returns:
            str: The HTML source of the current page.
        """
        return self.driver.page_source

    def close(self) -> None:
        """Close the browser and end the WebDriver session."""
        self.driver.quit()

    def wait_for_url(self, substring: str, timeout: int = 2) -> bool:
        """Wait until the current URL contains a given substring.

        Args:
            substring (str): The substring to check for in the URL.
            timeout (int): Maximum time to wait in seconds. Defaults to 2.

        Returns:
            bool: True if the URL contained the substring within the timeout,
            False otherwise.
        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains(substring))
            return True
        except Exception:
            return False
