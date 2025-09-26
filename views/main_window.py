# views/main_window.py
import tkinter as tk
from typing import Callable
import threading


class MainWindow(tk.Tk):
    """Main application window for the MSU Grades app.

    This class extends Tkinter's `Tk` and provides:
      - Routing (frame navigation)
      - Background execution of tasks to avoid UI freezing
      - A central container for all frames
      - Common style and geometry management
    """

    def __init__(self):
        """Initialize the main application window."""
        super().__init__()
        self.title("MSU Grades")
        self.geometry("840x560")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.frames = {}

        # Configure grid expansion for container
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def register_frame(self, name: str, frame: tk.Frame):
        """Register a frame with the main window.

        Args:
            name (str): The route name for the frame.
            frame (tk.Frame): The Tkinter frame to register.
        """
        self.frames[name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def navigate_to(self, name: str):
        """Navigate to a registered frame by name.

        Args:
            name (str): The route name of the target frame.

        Raises:
            KeyError: If the given name is not registered.
        """
        frame = self.frames[name]
        frame.tkraise()

        # Resize to frame's preferred geometry
        self.geometry(frame.geometry_config())

    def run_in_background(self, func: Callable):
        """Run a function in a background thread.

        This prevents the UI from freezing during long-running tasks.

        Args:
            func (Callable): The function to execute in the background.
        """
        t = threading.Thread(target=func, daemon=True)
        t.start()
