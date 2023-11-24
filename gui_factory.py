import tkinter as tk

from components.bot_container_component import BotContainerComponent

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
        
    def get_button(self, parent: tk.Canvas, icon: str, event=None) -> tk.Button:
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
        return button
    
    def get_bot_container(self, parent: tk.Canvas, coordinates: tuple, bot_instance) -> BotContainerComponent:
        play_btn = self.get_button(parent=parent, icon="play", event=lambda: bot_instance.start()) 
        setting_btn = self.get_button(parent=parent, icon="settings")
        delete_btn = self.get_button(parent=parent, icon="delete")
        
        return BotContainerComponent(parent=parent,
                                     coordinates=coordinates,
                                     buttons= [play_btn, setting_btn, delete_btn],
                                     bot=bot_instance)
    