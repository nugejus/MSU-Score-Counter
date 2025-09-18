# views/login_view.py
import tkinter as tk
from tkinter import ttk
from typing import Callable

class LoginView(tk.Frame):
    """
    Presenter가 기대하는 메서드:
    - on_submit(cb)
    - set_loading(flag: bool)
    - show_error(msg: str)
    - navigate_to(route: str)
    - run_in_background(func)
    """
    def __init__(self, parent):
        super().__init__(parent)
        self._on_submit: Callable[[str, str], None] | None = None

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        title = ttk.Label(self, text="Login to MSU Cabinet", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(24, 12))

        ttk.Label(self, text="Email").grid(row=1, column=0, sticky="e", padx=8, pady=6)
        ttk.Label(self, text="Password").grid(row=2, column=0, sticky="e", padx=8, pady=6)

        self.email_var = tk.StringVar()
        self.pw_var = tk.StringVar()
        self.email_entry = ttk.Entry(self, textvariable=self.email_var, width=32)
        self.pw_entry = ttk.Entry(self, textvariable=self.pw_var, width=32, show="*")

        self.email_entry.grid(row=1, column=1, sticky="w", padx=8, pady=6)
        self.pw_entry.grid(row=2, column=1, sticky="w", padx=8, pady=6)

        self.login_btn = ttk.Button(self, text="Login", command=self._submit_clicked)
        self.login_btn.grid(row=3, column=1, sticky="w", padx=8, pady=(12, 6))

        self.status_var = tk.StringVar(value="")
        self.status_label = ttk.Label(self, textvariable=self.status_var, foreground="#cc0000")
        self.status_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=8, pady=(4, 0))

        # 편의: Enter로 로그인
        self.pw_entry.bind("<Return>", lambda _: self._submit_clicked())

    # ---------- View <-> Presenter 계약 ----------
    def on_submit(self, cb: Callable[[str, str], None]):
        self._on_submit = cb

    def set_loading(self, flag: bool):
        self.login_btn.configure(state="disabled" if flag else "normal")
        self.status_var.set("Signing in..." if flag else "")

    def show_error(self, msg: str):
        self.status_var.set(msg)

    def navigate_to(self, route: str):
        # MainWindow에 위임
        self.master.master.navigate_to(route)

    def run_in_background(self, func):
        # MainWindow에 위임
        self.master.master.run_in_background(func)

    # ---------- 내부 ----------
    def _submit_clicked(self):
        if self._on_submit:
            email = self.email_var.get().strip()
            pw = self.pw_var.get()
            self._on_submit(email, pw)
