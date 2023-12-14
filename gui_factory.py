import tkinter as tk

from components.custom_input import CustomInput

class GUIFactory:
    
    @staticmethod
    def get_canvas(parent: tk.Tk, classes: tuple) -> dict:
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
    
    @staticmethod
    def get_subcanvas(parent: tk.Canvas, dimensions: tuple) -> tk.Canvas:
        return tk.Canvas(parent,
                    bg = "#112C5F",
                    height = dimensions[1],
                    width = dimensions[0],
                    bd = 0,
                    highlightthickness = 0,
                    relief = "ridge")
    
    @staticmethod    
    def get_button(parent: tk.Canvas, icon: str, isEnabled: bool = False, event=None) -> tk.Button:
        img = tk.PhotoImage(file=f'.\\assets\\icons\\{icon}.png')
        button = tk.Button(
            parent,
            image=img,
            borderwidth=0,
            highlightthickness=0,
            command=event,
            relief="flat"
        )
        button.image = img
        button.isEnabled = isEnabled
        return button
    
    @staticmethod   
    def get_custom_input(parent: tk.Canvas) -> CustomInput:
        img = tk.PhotoImage(file='.\\assets\\icons\\entry.png')
        return CustomInput(parent=parent,
                           image=img,
                           bd=0,
                           bg="#CFE2FF",
                           fg="#000716",
                           highlightthickness=0)
    
    @staticmethod    
    def set_text_in_canvas(parent: tk.Canvas, text: str, coordinates: tuple, size: int) -> int:
        return parent.create_text(
            coordinates[0], coordinates[1],
            anchor="nw",
            text=text,
            fill="#FFFFFF",
            font=("RobotoRoman ExtraBold", size * -1)
        )
    