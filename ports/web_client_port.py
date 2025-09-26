# ports/web_client_port.py
from typing import Protocol


class WebClientPort(Protocol):
    """Port interface for a web client.

    This protocol defines the methods required to automate
    browser interactions such as opening pages, waiting,
    typing into inputs, clicking elements, and retrieving HTML.

    Concrete implementations may use Selenium, Playwright,
    or any other automation library.
    """

    def open(self, url: str) -> None:
        """Open a URL in the web client.

        Args:
            url (str): The target URL to load.
        """

    def wait(self, seconds: float) -> None:
        """Pause execution for a given amount of time.

        Args:
            seconds (float): Duration to wait in seconds.
        """

    def find_and_type(
        self, by: str, selector: str, text: str, paste: bool = False
    ) -> None:
        """Find an element and type text into it.

        Args:
            by (str): Locator strategy (e.g., "name", "css", "link").
            selector (str): The element selector string.
            text (str): The text to type.
            paste (bool): If True, simulate paste action instead of keystrokes.
        """

    def click(self, by: str, selector: str) -> None:
        """Find an element and click it.

        Args:
            by (str): Locator strategy (e.g., "name", "css", "link").
            selector (str): The element selector string.
        """

    def page_source(self) -> str:
        """Return the current page's HTML source.

        Returns:
            str: The HTML content of the current page.
        """

    def close(self) -> None:
        """Close the client and release all resources."""

    def current_url(self) -> str:
        """Return the current browser URL.

        Returns:
            str: The current URL string.
        """

    def wait_for_url(self, substring: str, timeout: int = 10) -> bool:
        """Wait until the current URL contains a given substring.

        Args:
            substring (str): Substring to wait for in the URL.
            timeout (int): Maximum time to wait in seconds. Defaults to 10.

        Returns:
            bool: True if the URL contained the substring within timeout,
            False otherwise.
        """
