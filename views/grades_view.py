# views/grades_view.py
import tkinter as tk
from tkinter import ttk
from typing import Callable
# from domain.models import GradeEntry  # 타입 힌트용 (없어도 동작엔 영향 X)

class GradesView(tk.Frame):
    """
    Presenter가 기대하는 메서드:
    - on_refresh(cb)
    - set_loading(flag: bool)
    - show_error(msg: str)
    - render_grades(grades: list[GradeEntry])
    - render_gpa(gpa_results: list)
    - run_in_background(func)
    """
    def __init__(self, parent):
        super().__init__(parent)
        self._on_refresh: Callable[[], None] | None = None

        # 상단 바
        top = ttk.Frame(self)
        top.pack(fill="x", padx=8, pady=8)

        ttk.Label(top, text="Grades", font=("Segoe UI", 14, "bold")).pack(side="left")
        self.refresh_btn = ttk.Button(top, text="Calculate", command=self._refresh_clicked)
        self.refresh_btn.pack(side="right", padx=4)

        # 상태/에러
        second_top = ttk.Frame(self)
        second_top.pack(fill="x", padx=8, pady =0)
        self.status_var = tk.StringVar(value="")
        ttk.Label(second_top, textvariable=self.status_var).pack(side="left")

        self.diploma_only_check = tk.IntVar(value = 0)
        self.diploma_only_button = ttk.Checkbutton(second_top, text = "diploma only", variable=self.diploma_only_check)
        self.diploma_only_button.pack(side = "right")

        # 성적 테이블
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=8, pady=(6, 6))

        cols = ("subject", "mark")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=12)
        self.tree.heading("subject", text="Subject")
        self.tree.heading("mark", text="Mark")
        self.tree.column("subject", width=480)
        self.tree.column("mark", width=120, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)

        # GPA 결과
        gpa_frame = ttk.Frame(self)
        gpa_frame.pack(fill="x", padx=8, pady=(6, 12))
        ttk.Label(gpa_frame, text="GPA", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w")

        self.gpa_text = tk.Text(gpa_frame, height=4)
        self.gpa_text.grid(row=1, column=0, sticky="we", pady=(4, 0))
        gpa_frame.columnconfigure(0, weight=1)

    # ---------- View <-> Presenter 계약 ----------
    def on_refresh(self, cb: Callable[[], None]):
        self._on_refresh = cb

    def set_loading(self, flag: bool):
        self.refresh_btn.configure(state="disabled" if flag else "normal")
        self.status_var.set("Fetching..." if flag else "")

    def show_error(self, msg: str):
        self.status_var.set(msg)

    # def render_grades(self, grades: list[GradeEntry]):
    def render_grades(self, grades: list):
        # 기존 데이터 초기화
        for item in self.tree.get_children():
            self.tree.delete(item)
        # 채우기
        for g in grades:
            self.tree.insert("", "end", values=(g.subject, g.mark.value))

    def render_gpa(self, gpa_results: list):
        self.gpa_text.configure(state="normal")
        self.gpa_text.delete("1.0", "end")
        for r in gpa_results:
            self.gpa_text.insert("end", f"{r.scheme_name}: {r.value} ({r.count} subjects)\n")
        self.gpa_text.configure(state="disabled")

    def run_in_background(self, func):
        self.master.master.run_in_background(func)

    # ---------- 내부 ----------
    def _refresh_clicked(self):
        if self._on_refresh:
            self._on_refresh(self.diploma_only_check.get())

    def geometry_config(self):
        return "840x560"
    
if __name__ == "__main__":
    import tkinter as tk
    from tkinter import ttk

    # --- 더미 데이터/타입 ---
    class DummyGPA:
        def __init__(self, name, value, count):
            self.scheme_name = name
            self.value = value
            self.count = count

    class Mark:
        EXCELLENT = type("M", (), {"value": "отлично"})
        GOOD      = type("M", (), {"value": "хорошо"})
        SATISFACTORY = type("M", (), {"value": "удов."})

    class GradeEntry:
        def __init__(self, subject, mark):
            self.subject = subject
            self.mark = mark

    # --- 앱 부트 ---
    root = tk.Tk()
    root.title("GradesView Fake Run")

    view = GradesView(root)
    view.pack(fill="both", expand=True)
    root.geometry(view.geometry_config())

    # 초기 성적 렌더
    sample_grades = [
        GradeEntry("Физиология", Mark.EXCELLENT),
        GradeEntry("Гистология", Mark.GOOD),
        GradeEntry("Химия", Mark.SATISFACTORY),
    ]
    view.render_grades(sample_grades)

    # on_refresh 더미: 체크박스 상태 반영해 GPA 계산 흉내
    def fake_refresh():
        view.set_loading(True)
        # diploma_only 체크 여부
        only = bool(view.diploma_only_check.get())

        # 더미 GPA 결과
        gpas = [
            DummyGPA("5.0", 4.56 if not only else 4.80, len(sample_grades)),
            DummyGPA("4.5", 3.98 if not only else 4.20, len(sample_grades)),
            DummyGPA("4.3", 3.80 if not only else 4.05, len(sample_grades)),
        ]
        view.render_gpa(gpas)
        view.set_loading(False)
        view.status_var.set("Calculated (diploma only: %s)" % ("ON" if only else "OFF"))

    view.on_refresh(fake_refresh)

    # 시작 메시지
    view.status_var.set("Ready. Click 'Calculate'.")

    root.mainloop()
