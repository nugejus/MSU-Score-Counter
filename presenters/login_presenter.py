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
        self.view.set_loading(True)

        def job():
            ok = self.login_uc.execute(email=email, password=password)
            if ok:
                self.view.navigate_to("grades")
            else:
                self.view.show_error("로그인 실패")
            self.view.set_loading(False)

        self.view.run_in_background(job)
