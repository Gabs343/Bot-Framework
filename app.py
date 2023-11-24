import tkinter as tk
import time
import os

from gui_factory import GUIFactory
from canvas.principal_canvas import PrincipalCanvas

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        tk.Tk.__init__(self, *args, **kwargs)
        self.__bots_folder_path = '.\\bots'
        self.__gui_factory: GUIFactory = GUIFactory()
        
        self.title('App')
        self.geometry('1036x565')
        self.resizable(False, False)
        self.configure(bg = '#112C5F')
        
        self.__current_canvas = None
        
        self.__canvas_objects = self.__gui_factory.get_canvas(parent=self, 
                                                              classes=(PrincipalCanvas, ))
        
        self.show_canvas('PrincipalCanvas')
        
    @property
    def gui_factory(self) -> GUIFactory:
        return self.__gui_factory
    
    @property
    def bots_folder_path(self) -> str:
        return self.__bots_folder_path
        
    def show_canvas(self, name: str):
        if self.__current_canvas:
            self.__current_canvas.pack_forget()
            
        self.__current_canvas = self.__canvas_objects[name]
        self.__current_canvas.pack()
        
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
        