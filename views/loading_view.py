import tkinter as tk
from tkinter import ttk


class LoadingView(tk.Frame):
    """Tkinter-based loading view.

    This view displays a simple status message in the center
    of the window. It is typically used to indicate initialization
    or background processing steps (e.g., preparing the client
    or parser).
    """

    def __init__(self, parent):
        """Initialize the LoadingView.

        Args:
            parent: Parent Tkinter widget.
        """
        super().__init__(parent)
        self.status_var = tk.StringVar(value="")
        self.status_label = ttk.Label(self, textvariable=self.status_var)
        self.status_label.pack(expand=True)

    def set_status(self, msg: str):
        """Update the status message.

        Args:
            msg (str): The status text to display.
        """
        self.status_var.set(msg)

    def geometry_config(self) -> str:
        """Return the default geometry for this view.

        Returns:
            str: Geometry string (e.g., "300x100").
        """
        return "300x100"
