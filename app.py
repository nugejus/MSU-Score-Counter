from views import MainWindow, LoginView, GradesView, LoadingView
from adapter import SeleniumClient, BsParser
from usecase import LoginUseCase, FetchGradesUseCase, ComputeGpaUseCase
from presenters import LoginPresenter, GradesPresenter

import config


def create_app():
    """Create and initialize the MSU Grades application.

    This function bootstraps the application by:
      - Creating the main window
      - Displaying a loading screen
      - Initializing the Selenium client
      - Initializing the parser and use cases
      - Wiring up presenters with their respective views

    Returns:
        tuple:
            - MainWindow: The root Tkinter application window
            - SeleniumClient: The web client instance
    """
    root = MainWindow()
    loading_view = LoadingView(root.container)

    # Show loading screen first
    root.register_frame("loading", loading_view)
    root.navigate_to("loading")

    loading_view.set_status("Preparing client....")
    client = SeleniumClient()

    def bootstrap():
        """Background initialization of parser, use cases, and presenters."""
        loading_view.set_status("Preparing Parser....")
        parser = BsParser()

        loading_view.set_status("Preparing usecases....")
        login_uc = LoginUseCase(client, base_url=config.MSU_LOGIN_URL)
        fetch_uc = FetchGradesUseCase(client, parser)
        gpa_uc = ComputeGpaUseCase()

        def wire_up():
            """Wire up views with presenters and navigate to login view."""
            login_view = LoginView(root.container)
            grades_view = GradesView(root.container)

            root.register_frame("login", login_view)
            root.register_frame("grades", grades_view)
            root.navigate_to("login")

            LoginPresenter(login_view, login_uc)
            GradesPresenter(grades_view, fetch_uc, gpa_uc)

        # Schedule wiring up on the main UI thread
        root.after(0, wire_up)

    # Run bootstrap asynchronously to avoid freezing
    root.run_in_background(bootstrap)
    return root, client


if __name__ == "__main__":
    root_, client_ = create_app()
    try:
        root_.mainloop()
    finally:
        client_.close()
