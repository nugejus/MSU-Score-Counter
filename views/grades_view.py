# views/grades_view.py
import tkinter as tk
from tkinter import ttk
from typing import Callable
from domain.models import GradeEntry  # 타입 힌트용 (없어도 동작엔 영향 X)

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
        self.refresh_btn = ttk.Button(top, text="Refresh", command=self._refresh_clicked)
        self.refresh_btn.pack(side="right", padx=4)

        # 상태/에러
        self.status_var = tk.StringVar(value="")
        ttk.Label(self, textvariable=self.status_var).pack(anchor="w", padx=8)

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

    def render_grades(self, grades: list[GradeEntry]):
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
            self._on_refresh()

    def geometry_config(self):
        return "840x560"