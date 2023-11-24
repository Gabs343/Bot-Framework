import tkinter as tk

class PrincipalCanvas(tk.Canvas): 
    def __init__(self, parent, **kwargs) -> None:
        tk.Canvas.__init__(parent, **kwargs)