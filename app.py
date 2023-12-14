import tkinter as tk
import time
import os

from gui_factory import GUIFactory
from canvas.principal_canvas import PrincipalCanvas
from canvas.settings_canvas import SettingCanvas

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.__bots_folder_path: str = '.\\bots'
        self.__current_canvas: tk.Canvas = None
        
        self.title('App')
        self.geometry('1036x565')
        self.resizable(width=False, height=False)
        self.configure(bg = '#112C5F')
   
        self.__canvas_objects: dict = GUIFactory.get_canvas(parent=self, 
                                                                    classes=(PrincipalCanvas, SettingCanvas))
        
        self.show_canvas(name='PrincipalCanvas')
    
    @property
    def bots_folder_path(self) -> str:
        return self.__bots_folder_path
        
    def show_canvas(self, name: str, **kwargs):
        if(self.__current_canvas):
            self.__current_canvas.pack_forget()
            
        self.__current_canvas = self.__canvas_objects[name]
        self.__current_canvas.pack()
        if(kwargs):
            self.__current_canvas.show_settings(bot_folder=kwargs["bot_folder"], 
                                                settings=kwargs["settings"])
        
    def create_bots_folder(self) -> None:
        if(not os.path.exists(self.__bots_folder_path)):
            os.makedirs(self.__bots_folder_path)
        
def main():
    app = MainApp()
    app.mainloop()
     
if __name__ == "__main__":
    st = time.time()
    main()
    et = time.time()
    elapsed_time = et - st
    print("Exceution time:", elapsed_time, "seconds")
        