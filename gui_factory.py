import tkinter as tk

class GUIFactory:
    
    def get_canvas(self, parent: tk.Tk, classes: tuple) -> dict:
        canvas = {}
        for cls in classes:
            canvas[cls.__name__] = cls(parent,
                                        bg = "#112C5F",
                                        height = 565,
                                        width = 1036,
                                        bd = 0,
                                        highlightthickness = 0,
                                        relief = "ridge")
        return canvas
    
    def get_subcanvas(self, parent: tk.Canvas) -> tk.Canvas:
        return tk.Canvas(parent,
                    bg = "#112C5F",
                    height = 335,
                    width = 897,
                    bd = 0,
                    highlightthickness = 0,
                    relief = "ridge")
    