
from ports import WebClientPort
import config
import time

class LoginUseCase:
    def __init__(self, client : WebClientPort , base_url: str):
        self.client = client
        self.base_url = base_url

    def execute(self, email: str, password: str) -> tuple[bool, str]:
        """
        로그인 시도 후 (성공여부, 메시지) 반환.
        메시지는 실패 시 사용자에게 보여줄 친절한 문구.
        """
        self.client.open(self.base_url)
        self.client.wait(0.5)

        self.client.find_and_type("name", "LoginForm[email]", email)
        self.client.find_and_type("name", "LoginForm[password]", password)
        self.client.click("name", "login-button")

        # 로그인 결과 대기 (성공/실패 신호 중 하나가 뜰 때까지)
        deadline = time.time() + config.LOGIN_POSTWAIT_SEC
        error_snippet = ""

        while time.time() < deadline:
            # 1) 성공 신호 체크
            for by, sel in config.LOGIN_SUCCESS_PROBES:
                if self.client.exists(by, sel):
                    return True, ""

            # 2) 에러 신호 체크 (보이면 즉시 실패 반환)
            for by, sel in config.LOGIN_ERROR_PROBES:
                if self.client.exists(by, sel):
                    # 에러 텍스트 있으면 추출
                    t = self.client.text(by, sel)
                    if t:
                        error_snippet = t
                    return False, error_snippet or "로그인에 실패했습니다. 아이디/비밀번호를 확인하세요."

            self.client.wait(0.2)

        # 여기까지 왔다면 둘 다 못 찾음 → 타임아웃 또는 UI 변경
        return False, "로그인 결과를 확인하지 못했습니다. 네트워크 상태나 사이트 UI 변경을 확인하세요."

