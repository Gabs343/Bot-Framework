import tkinter as tk
import time
import os

from gui_factory import GUIFactory
from canvas.principal_canvas import PrincipalCanvas

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        tk.Tk.__init__(self, *args, **kwargs)
        self.gui_factory: GUIFactory = GUIFactory()
        
        self.title("App")
        self.geometry("1036x565")
        self.resizable(False, False)
        self.configure(bg = "#112C5F")
        
        self.current_canvas = None
        
        self.canvas_objects = self.gui_factory.get_canvas(self, (PrincipalCanvas, ))
        
        self.show_canvas("PrincipalCanvas")
        
    def show_canvas(self, name: str):
        if self.current_canvas:
            self.current_canvas.pack_forget()
            
        self.current_canvas = self.canvas_objects[name]
        self.current_canvas.pack()
        
def main():
    app = MainApp()
    app.mainloop()
     
if __name__ == "__main__":
    st = time.time()
    main()
    et = time.time()
    elapsed_time = et - st
    print("Exceution time:", elapsed_time, "seconds")
        