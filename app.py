from views import MainWindow, LoginView, GradesView, LoadingView
from adapter import SeleniumClient, BsParser
from usecase import LoginUseCase, FetchGradesUseCase, ComputeGpaUseCase
from presenters import LoginPresenter, GradesPresenter

import config

def create_app():
    root = MainWindow()
    loading_view = LoadingView(root.container)

    root.register_frame("loading", loading_view)
    root.navigate_to("loading")

    def bootstrap():
        loading_view.set_status("Preparing client....")
        client = SeleniumClient()

        loading_view.set_status("Preparing Parser....")
        parser = BsParser()

        loading_view.set_status("Preparing usecases....")
        login_uc = LoginUseCase(client, base_url=config.MSU_LOGIN_URL)
        fetch_uc = FetchGradesUseCase(client, parser)
        gpa_uc = ComputeGpaUseCase()

        def wire_up():
            login_view = LoginView(root.container)
            grades_view = GradesView(root.container)

            root.register_frame("login", login_view)
            root.register_frame("grades", grades_view)
            root.navigate_to("login")

    # Presenters

            LoginPresenter(login_view, login_uc)
            GradesPresenter(grades_view, fetch_uc, gpa_uc)  # gpa_uc 없으면 Presenter 수정 필요
        
        root.after(0,wire_up)
    root.run_in_background(bootstrap)
    return root

if __name__ == "__main__":
    root = create_app()
    try:
        root.mainloop()
    finally:
        root.client.close()
