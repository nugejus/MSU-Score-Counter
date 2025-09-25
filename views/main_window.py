# views/main_window.py
import tkinter as tk
from typing import Callable
import threading

class MainWindow(tk.Tk):
    """
    - 라우팅(프레임 전환)
    - 백그라운드 실행(run_in_background)
    - 공통 스타일 적용 지점
    """
    def __init__(self):
        super().__init__()
        self.title("MSU Grades")
        self.geometry("840x560")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.frames = {}

        # grid 확장
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def register_frame(self, name: str, frame: tk.Frame):
        self.frames[name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def navigate_to(self, name: str):
        frame = self.frames[name]
        frame.tkraise()

        self.geometry(frame.geometry_config())

    def run_in_background(self, func: Callable):
        """UI 프리징 방지용"""
        t = threading.Thread(target=func, daemon=True)
        t.start()