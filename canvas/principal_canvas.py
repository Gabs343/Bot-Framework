import tkinter as tk

from gui_factory import GUIFactory

class PrincipalCanvas(tk.Canvas): 
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        
        self.parent = parent
        self.gui_factory: GUIFactory = parent.gui_factory
        
        self.subcanvas = self.gui_factory.get_subcanvas(self)
        self.subcanvas.place(x=75, y=75)
        
        add_btn = self.gui_factory.get_button(parent=self, icon="add", event= lambda: print("add bot"))
        add_btn.place(
            x=495.0,
            y=433.0,
            width=70.0,
            height=70.0
        )
        
        refresh_btn = self.gui_factory.get_button(parent=self, icon="refresh", event= lambda: print("reload container"))
        refresh_btn.place(
            x=915.0,
            y=29.0,
            width=50.0,
            height=50.0
        )