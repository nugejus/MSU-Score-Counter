from views import MainWindow, LoginView, GradesView
from adapter import SeleniumClient, BsParser
from usecase import LoginUseCase, FetchGradesUseCase

import config

def create_app():
    # Adapters
    client = SeleniumClient()
    parser = BsParser()

    # UseCases
    login_uc = LoginUseCase(client, base_url=config.MSU_LOGIN_URL)
    fetch_uc = FetchGradesUseCase(client, parser)

    # (옵션) GPA 유스케이스 연결
    try:
        from usecase import ComputeGpaUseCase
        gpa_uc = ComputeGpaUseCase()
    except ModuleNotFoundError:
        gpa_uc = None

    # Views
    root = MainWindow()
    login_view = LoginView(root.container)
    grades_view = GradesView(root.container)

    root.register_frame("login", login_view)
    root.register_frame("grades", grades_view)
    root.navigate_to("login")

    # Presenters
    from presenters import LoginPresenter, GradesPresenter

    LoginPresenter(login_view, login_uc)
    GradesPresenter(grades_view, fetch_uc, gpa_uc)  # gpa_uc 없으면 Presenter 수정 필요

    return root, client

if __name__ == "__main__":
    root, client = create_app()
    try:
        root.mainloop()
    finally:
        client.close()
