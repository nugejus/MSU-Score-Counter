import tkinter as tk

class LoadingView(tk.Frame):
    def __init__(self, parent):
        super.__init__(parent)

    def geometry_config(self):
        return "300x100"