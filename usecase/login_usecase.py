
from ports import WebClientPort

class LoginUseCase:
    def __init__(self, client : WebClientPort , base_url: str):
        self.client = client
        self.base_url = base_url
        self.client.open(self.base_url)

    def execute(self, email: str, password: str) -> bool:
        """
        로그인 시도 후 (성공여부, 메시지) 반환.
        메시지는 실패 시 사용자에게 보여줄 친절한 문구.
        """
        self.client.find_and_type("name", "LoginForm[email]", email)
        self.client.find_and_type("name", "LoginForm[password]", password)

        self.client.click("name", "login-button")
        if not self.client.wait_for_url("https://lk.msu.ru/cabinet"):
            return False

        self.client.click("link", "Оценки")
        return self.client.wait_for_url("https://lk.msu.ru/cabinet/marks")
