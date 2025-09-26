# views/grades_view.py
import tkinter as tk
from tkinter import ttk
from typing import Callable

# from domain.models import GradeEntry  # 타입 힌트용 (없어도 동작엔 영향 X)


class GradesView(tk.Frame):
    """Tkinter-based view for displaying grades and GPA results.

    This view is controlled by a presenter (GradesPresenter) and
    exposes methods expected by the presenter to update UI state,
    show errors, render grade tables, and render GPA results.

    Expected presenter calls:
        - on_refresh(cb)
        - set_loading(flag: bool)
        - show_error(msg: str)
        - render_grades(grades: list[GradeEntry])
        - render_gpa(gpa_results: list[GPAResult])
        - run_in_background(func)
    """

    def __init__(self, parent):
        """Initialize the GradesView.

        Args:
            parent: Parent Tkinter widget.
        """
        super().__init__(parent)
        self._on_refresh: Callable[[], None] | None = None

        # Top bar with title and refresh button
        top = ttk.Frame(self)
        top.pack(fill="x", padx=8, pady=8)

        ttk.Label(top, text="Grades", font=("Segoe UI", 14, "bold")).pack(side="left")
        self.refresh_btn = ttk.Button(
            top, text="Calculate", command=self._refresh_clicked
        )
        self.refresh_btn.pack(side="right", padx=4)

        # Status and options
        second_top = ttk.Frame(self)
        second_top.pack(fill="x", padx=8, pady=0)
        self.status_var = tk.StringVar(value="")
        ttk.Label(second_top, textvariable=self.status_var).pack(side="left")

        self.diploma_only_check = tk.IntVar(value=0)
        self.diploma_only_button = ttk.Checkbutton(
            second_top, text="diploma only", variable=self.diploma_only_check
        )
        self.diploma_only_button.pack(side="right")

        # Grade table
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

        # GPA results
        gpa_frame = ttk.Frame(self)
        gpa_frame.pack(fill="x", padx=8, pady=(6, 12))
        ttk.Label(gpa_frame, text="GPA", font=("Segoe UI", 12, "bold")).grid(
            row=0, column=0, sticky="w"
        )

        self.gpa_text = tk.Text(gpa_frame, height=4)
        self.gpa_text.grid(row=1, column=0, sticky="we", pady=(4, 0))
        gpa_frame.columnconfigure(0, weight=1)

    # ---------- View <-> Presenter 계약 ----------
    def on_refresh(self, cb: Callable[[], None]):
        """Register a callback for the refresh event.

        Args:
            cb (Callable[[], None]): Callback to invoke when refresh is triggered.
        """
        self._on_refresh = cb

    def set_loading(self, flag: bool):
        """Set the loading state of the view.

        Args:
            flag (bool): True to show loading (disable refresh button
                and show status text), False to reset.
        """
        self.refresh_btn.configure(state="disabled" if flag else "normal")
        self.status_var.set("Fetching..." if flag else "")

    def show_error(self, msg: str):
        """Display an error message in the status area.

        Args:
            msg (str): Error message to display.
        """
        self.status_var.set(msg)

    def render_grades(self, grades: list):
        """Render grade entries in the table.

        Args:
            grades (list[GradeEntry]): List of grade entries to display.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)
        for g in grades:
            self.tree.insert("", "end", values=(g.subject, g.mark.value))

    def render_gpa(self, gpa_results: list):
        """Render GPA results in the text box.

        Args:
            gpa_results (list[GPAResult]): List of GPA results to display.
        """
        self.gpa_text.configure(state="normal")
        self.gpa_text.delete("1.0", "end")
        for r in gpa_results:
            self.gpa_text.insert(
                "end", f"{r.scheme_name}: {r.value} ({r.count} subjects)\n"
            )
        self.gpa_text.configure(state="disabled")

    def run_in_background(self, func):
        """Delegate background task execution to the main window.

        Args:
            func (Callable): Function to run in the background thread.
        """
        self.master.master.run_in_background(func)

    # ---------- 내부 ----------
    def _refresh_clicked(self):
        """Handle the Calculate button click.

        Invokes the registered refresh callback with the current
        diploma_only setting.
        """
        if self._on_refresh:
            self._on_refresh(self.diploma_only_check.get())

    def geometry_config(self):
        """Return the default geometry string for this view.

        Returns:
            str: Geometry string (e.g., "840x560").
        """
        return "840x560"
