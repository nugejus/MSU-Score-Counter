# presenters/grades_presenter.py
from usecase import FetchGradesUseCase, ComputeGpaUseCase

class GradesPresenter:
    def __init__(self, view, fetch_uc: FetchGradesUseCase, gpa_uc: ComputeGpaUseCase):
        """
        view : GradesView 객체 (Tkinter 등)
        fetch_uc : 성적 가져오기 유스케이스
        gpa_uc : GPA 계산 유스케이스
        """
        self.view = view
        self.fetch_uc = fetch_uc
        self.gpa_uc = gpa_uc

        self.view.on_refresh(self.handle_refresh)

    def handle_refresh(self, diploma_only):
        self.view.set_loading(True)

        def job():
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
