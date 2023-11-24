import tkinter as tk

from gui_factory import GUIFactory

class PrincipalCanvas(tk.Canvas): 
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        
        self.parent = parent
        self.gui_factory: GUIFactory = parent.gui_factory
        
        self.subcanvas = self.gui_factory.get_subcanvas(self)
        self.subcanvas.place(x=75, y=75)