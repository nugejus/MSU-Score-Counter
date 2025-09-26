# presenters/login_presenter.py
from usecase import LoginUseCase


class LoginPresenter:
    """Presenter for handling the login process.

    This presenter connects the LoginView (UI) with the LoginUseCase.
    It listens for user input events (email/password submission),
    executes the login process in the background, and updates the view
    accordingly (success → navigate to grades, failure → show error).
    """

    def __init__(self, view, login_uc: LoginUseCase):
        """Initialize the LoginPresenter.

        Args:
            view: The LoginView object (Tkinter, PySide, or similar).
            login_uc (LoginUseCase): The use case responsible for login.
        """
        self.view = view
        self.login_uc = login_uc

        # Register the submit handler with the view
        self.view.on_submit(self.handle_submit)

    def handle_submit(self, email: str, password: str):
        """Handle the login form submission.

        This method:
        - Puts the view into a loading state.
        - Runs a background job to execute the login use case.
        - On success: navigates to the "grades" view.
        - On failure: shows an error message.
        - Restores the loading state at the end.

        Args:
            email (str): User email (login ID).
            password (str): User password.
        """
        self.view.set_loading(True)

        def job():
            """Background job that performs the login and updates the view."""
            ok = self.login_uc.execute(email=email, password=password)
            if ok:
                self.view.navigate_to("grades")
            else:
                self.view.show_error("Incorrect id or pw")
            self.view.set_loading(False)

        self.view.run_in_background(job)
