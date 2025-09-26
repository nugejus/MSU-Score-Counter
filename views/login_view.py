# views/login_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable


class LoginView(tk.Frame):
    """Tkinter-based login view.

    This view provides the UI for logging into the MSU Cabinet.
    It contains input fields for email and password, a login button,
    an exit button, and a status label. It is designed to be controlled
    by a presenter (LoginPresenter), which registers callbacks and
    manages navigation.
    """

    def __init__(self, parent):
        """Initialize the LoginView.

        Args:
            parent: The parent Tkinter widget.
        """
        super().__init__(parent)
        self._on_submit: Callable[[str, str], None] | None = None

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        title = ttk.Label(
            self, text="Login to MSU Cabinet", font=("Segoe UI", 16, "bold")
        )
        title.grid(row=0, column=0, columnspan=3, pady=(24, 12))

        ttk.Label(self, text="Email").grid(row=1, column=0, sticky="e", padx=8, pady=6)
        ttk.Label(self, text="Password").grid(
            row=2, column=0, sticky="e", padx=8, pady=6
        )

        self.email_var = tk.StringVar()
        self.pw_var = tk.StringVar()
        self.email_entry = ttk.Entry(self, textvariable=self.email_var, width=40)
        self.pw_entry = ttk.Entry(self, textvariable=self.pw_var, show="*", width=40)

        self.email_entry.grid(row=1, column=1, columnspan=2, sticky="w", padx=8, pady=6)
        self.pw_entry.grid(row=2, column=1, columnspan=2, sticky="w", padx=8, pady=6)

        self.login_btn = ttk.Button(self, text="Login", command=self._submit_clicked)
        self.login_btn.grid(row=3, column=1, sticky="e", padx=8, pady=(12, 6))

        self.exit_btn = ttk.Button(self, text="Exit", command=self._exit)
        self.exit_btn.grid(row=3, column=2, sticky="w", padx=8, pady=(12, 6))

        self.status_var = tk.StringVar(value="")
        self.status_label = ttk.Label(
            self, textvariable=self.status_var, foreground="#cc0000"
        )
        self.status_label.grid(
            row=4, column=0, columnspan=2, sticky="w", padx=8, pady=(4, 0)
        )

        # Allow Enter key to trigger login
        self.pw_entry.bind("<Return>", lambda _: self._submit_clicked())

    # ---------- View <-> Presenter contract ----------
    def on_submit(self, cb: Callable[[str, str], None]):
        """Register a callback for the submit event.

        Args:
            cb (Callable[[str, str], None]): Callback to be called with
                email and password when the user submits.
        """
        self._on_submit = cb

    def set_loading(self, flag: bool):
        """Set the loading state of the login view.

        Args:
            flag (bool): True to show loading state (disable login button
                and show status), False to reset.
        """
        self.login_btn.configure(state="disabled" if flag else "normal")
        self.status_var.set("Signing in..." if flag else "")

    def show_error(self, msg: str):
        """Display an error message.

        Args:
            msg (str): Error message to show in a popup dialog.
        """
        messagebox.showerror("Error", msg)

    def navigate_to(self, route: str):
        """Navigate to another route via the main window.

        Args:
            route (str): Target route name (e.g., "grades").
        """
        self.master.master.navigate_to(route)

    def run_in_background(self, func):
        """Run a function in the background via the main window.

        Args:
            func (Callable): Function to execute asynchronously.
        """
        self.master.master.run_in_background(func)

    # ---------- Internal ----------
    def _submit_clicked(self):
        """Handle the login button click or Enter key press."""
        if self._on_submit:
            email = self.email_var.get().strip()
            pw = self.pw_var.get()
            self._on_submit(email, pw)

    def geometry_config(self) -> str:
        """Return the default geometry string for the view.

        Returns:
            str: Geometry string (e.g., "500x200").
        """
        return "500x200"

    def _exit(self):
        """Exit the application by quitting the main window."""
        self.master.master.quit()
