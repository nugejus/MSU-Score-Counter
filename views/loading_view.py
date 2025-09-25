import tkinter as tk
from tkinter import ttk

class LoadingView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.status_var = tk.StringVar(value="")
        self.status_label = ttk.Label(self, textvariable=self.status_var)
        self.status_label.pack(expand=True)

    def set_status(self, msg):
        self.status_var.set(msg)

    def geometry_config(self):
        return "300x100"