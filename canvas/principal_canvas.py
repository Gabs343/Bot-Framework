import tkinter as tk

class PrincipalCanvas(tk.Canvas): 
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)