# presenters/grades_presenter.py
from usecase import FetchGradesUseCase, ComputeGpaUseCase


class GradesPresenter:
    """Presenter for coordinating grade fetching and GPA calculation.

    This presenter connects the GradesView (UI) with the use cases:
    - FetchGradesUseCase: retrieves grade entries from the web client/parser.
    - ComputeGpaUseCase: computes GPA values from grade entries.

    It registers event handlers on the view and orchestrates background jobs
    for smooth user experience.
    """

    def __init__(self, view, fetch_uc: FetchGradesUseCase, gpa_uc: ComputeGpaUseCase):
        """Initialize the GradesPresenter.

        Args:
            view: The GradesView object (Tkinter-based UI).
            fetch_uc (FetchGradesUseCase): Use case for fetching grades.
            gpa_uc (ComputeGpaUseCase): Use case for computing GPA values.
        """
        self.view = view
        self.fetch_uc = fetch_uc
        self.gpa_uc = gpa_uc

        # Register refresh handler with the view
        self.view.on_refresh(self.handle_refresh)

    def handle_refresh(self, diploma_only):
        """Handle refresh event from the view.

        Invoked when the user triggers grade refresh. This method:
        - Sets the view into loading state.
        - Runs a background job to fetch grades and compute GPA.
        - Renders the results or shows an error message.
        - Resets the loading state.

        Args:
            diploma_only (bool): If True, include only diploma-related results.
        """
        self.view.set_loading(True)

        def job():
            """Background job for fetching grades and computing GPA."""
            try:
                grades = self.fetch_uc.execute(diploma_only=diploma_only)
                gpas = self.gpa_uc.execute(grades)
                self.view.render_grades(grades)
                self.view.render_gpa(gpas)
            except Exception as e:
                self.view.show_error(f"Fetch failed: {e}")
            finally:
                self.view.set_loading(False)

        self.view.run_in_background(job)
