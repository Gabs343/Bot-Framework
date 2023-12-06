import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import threading
import os

from gui_factory import GUIFactory

class PrincipalCanvas(tk.Canvas): 
    def __init__(self, parent: tk.Tk, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        
        self.__parent: tk.Tk = parent
        self.__bot_instances: dict = {}
        self.__gui_factory: GUIFactory = parent.gui_factory
        
        self.create_gui_elements()
        
    def create_gui_elements(self) -> None:
        self.subcanvas: tk.Canvas = self.__gui_factory.get_subcanvas(parent=self, dimensions=(897, 335))
        self.subcanvas.place(x=75, y=75)
        
        add_btn: tk.Button = self.__gui_factory.get_button(parent=self, 
                                              icon='add', 
                                              event= lambda: self.add_bot())
        
        refresh_btn: tk.Button = self.__gui_factory.get_button(parent=self, 
                                                  icon='refresh', 
                                                  event= lambda: self.refresh())
        
        add_btn.place(
            x=495.0, y=433.0,
            width=70.0, height=70.0
        )
        
        refresh_btn.place(
            x=915.0, y=29.0,
            width=50.0, height=50.0
        )
        
        self.refresh()
        self.create_bots_containers()
        
    def create_bots_containers(self) -> None:
        y = 8.0
        for folder, bot_instance in self.__bot_instances.items():
            
            container = self.__gui_factory.get_bot_container(parent=self.subcanvas, 
                                                           coordinates=(77.0, y), 
                                                           bot_instance=bot_instance)
            
            container.set_button_event(button=0,
                                       event=lambda bot=bot_instance: self.start_bot(bot=bot))
            
            container.set_button_event(button=1, 
                                       event=lambda folder=folder, bot_instance=bot_instance: self.__parent.show_canvas(name='SettingCanvas',
                                                                                                       bot_folder=folder,
                                                                                                       settings=bot_instance.settings_services))
            container.set_button_event(button=2, 
                                       event=lambda folder=folder: self.delete_bot(folder=folder))
            
            y += 125.0
            
    def refresh(self) -> None:
        self.subcanvas.delete("all")
        self.__parent.create_bots_folder()
        bots_folders = [folder_name for folder_name in os.listdir(self.__parent.bots_folder_path)]
        new_instances = {}
    
        for folder in bots_folders:
            module = __import__(f'bots.{folder}.main', fromlist=['Main'])
            bot = getattr(module, 'Main')
            
            if(folder in self.__bot_instances):
                new_instances[folder] = self.__bot_instances[folder]
            else:
                new_instances[folder] = bot()

        self.__bot_instances = new_instances
        self.create_bots_containers()
        
    def add_bot(self) -> None:
        src_bot: str = filedialog.askdirectory()
        shutil.move(src_bot, self.__parent.bots_folder_path)
        self.refresh()
    
    def start_bot(self, bot) -> None:
        thread = threading.Thread(target=bot.start)
        thread.start()
            
    def delete_bot(self, folder: str) -> None:
        msg_delete: str = messagebox.askquestion('Delete Bot', 'Are you sure you want to delete this bot?',
                                icon='warning')
        if(msg_delete == "yes"):
            shutil.rmtree(f'{self.__parent.bots_folder_path}\\{folder}')
        self.refresh()