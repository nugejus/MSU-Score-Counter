
from ports import WebClientPort

class LoginUseCase:
    def __init__(self, client : WebClientPort , base_url: str):
        self.client = client
        self.base_url = base_url

    def execute(self, email: str, password: str):
        self.client.open(self.base_url)
        self.client.wait(1.0)
        self.client.find_and_type("name", "LoginForm[email]", email)
        self.client.find_and_type("name", "LoginForm[password]", password)
        self.client.click("name", "login-button")
        self.client.wait(2.0)

