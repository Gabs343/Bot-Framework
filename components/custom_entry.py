import tkinter as tk

class CustomInput(tk.Entry):
    def __init__(self, parent: tk.Canvas, image: tk.PhotoImage, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.image = image
        
        self.entry_width = 156.0
        self.entry_height = 32.0
        
    def set_label(self, text: str, coordinates: tuple):
        self.parent.create_text(
                    coordinates[0], 
                    coordinates[1],
                    anchor="nw",
                    text=text,
                    fill="#FFFFFF",
                    font=("RobotoRoman ExtraBold", 14 * -1)
        )
        
    def set_entry(self, coordinates: tuple):
        self.parent.create_window(
            coordinates[0],
            coordinates[1],
            width=156.0,
            height=32.0,
            window=self
        )
        
        self.parent.create_image(
            coordinates[0],
            coordinates[1]+2,
            image=self.image
        )
        
    

        
