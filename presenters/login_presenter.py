# presenters/login_presenter.py
from usecase import LoginUseCase

class LoginPresenter:
    def __init__(self, view, login_uc: LoginUseCase):
        """
        view : LoginView 객체 (Tkinter, PySide 등)
        login_uc : 로그인 유스케이스
        """
        self.view = view
        self.login_uc = login_uc
        # View에서 on_submit 이벤트 등록
        self.view.on_submit(self.handle_submit)

    def handle_submit(self, email: str, password: str):
        """
        View에서 로그인 버튼 눌렀을 때 실행
        """
        self.view.set_loading(True)

        def job():
            try:
                self.login_uc.execute(email=email, password=password)
                self.view.navigate_to("grades")  # 성공 시 화면 전환
            except Exception as e:
                self.view.show_error(f"Login failed: {e}")
            finally:
                self.view.set_loading(False)

        # UI 멈춤 방지를 위해 백그라운드 실행
        self.view.run_in_background(job)
