from ports import WebClientPort


class LoginUseCase:
    """Use case for handling login to the MSU Cabinet system.

    This use case automates the login process using the provided
    web client. It fills in the email and password, submits the form,
    and verifies whether login was successful.
    """

    def __init__(self, client: WebClientPort, base_url: str):
        """Initialize the LoginUseCase.

        Args:
            client (WebClientPort): A web client adapter (e.g., Selenium client).
            base_url (str): The login page URL for the MSU Cabinet.
        """
        self.client = client
        self.base_url = base_url
        self.client.open(self.base_url)

    def execute(self, email: str, password: str) -> bool:
        """Attempt to log in with the given credentials.

        This method fills in the login form with the provided
        email and password, clicks the login button, and checks
        whether the login was successful by verifying the URL.

        Args:
            email (str): The user's email address (login ID).
            password (str): The user's password.

        Returns:
            bool: True if login succeeded and the marks page was reached,
            False otherwise.

        Example:
            >>> usecase = LoginUseCase(client, "https://lk.msu.ru/cabinet")
            >>> success = usecase.execute("user@example.com", "password123")
            >>> print(success)
            True
        """
        self.client.find_and_type("name", "LoginForm[email]", email)
        self.client.find_and_type("name", "LoginForm[password]", password)

        self.client.click("name", "login-button")
        if not self.client.wait_for_url("https://lk.msu.ru/cabinet"):
            return False

        self.client.click("link", "Оценки")
        return self.client.wait_for_url("https://lk.msu.ru/cabinet/marks")
