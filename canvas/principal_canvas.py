import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import threading
import os

from gui_factory import GUIFactory
from components.bot_container_component import BotContainerComponent

class PrincipalCanvas(tk.Canvas): 
    def __init__(self, parent: tk.Tk, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        
        self.__parent: tk.Tk = parent
        self.__bot_instances: dict = {}
        
        self.create_gui_elements()
        
    def create_gui_elements(self) -> None:
        self.subcanvas: tk.Canvas = GUIFactory.get_subcanvas(parent=self, width=897, height=335, bg='#112C5F')
        self.subcanvas.place(x=75, y=75)
        
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.subcanvas.yview)
        
        self.subcanvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.place(x= 70 +897, y=75, height=385)
        
        add_btn: tk.Button = GUIFactory.get_button(parent=self, 
                                              icon='add', 
                                              event= lambda: self.add_bot())
        
        refresh_btn: tk.Button = GUIFactory.get_button(parent=self, 
                                                  icon='refresh', 
                                                  event= lambda: self.refresh())
        
        self.subcanvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.subcanvas.bind("<Configure>", self.on_configure)
        
        add_btn.place(
            x=495.0, y=433.0,
            width=70.0, height=70.0
        )
        
        refresh_btn.place(
            x=915.0, y=29.0,
            width=50.0, height=50.0
        )
        
        self.refresh()
        
    def on_configure(self, event=None) -> None:
        self.subcanvas.configure(scrollregion=self.subcanvas.bbox("all"))

    def on_mousewheel(self, event) -> None:
        if event.delta:
            self.subcanvas.yview_scroll(-1 * (event.delta // 120), "units")
        
    def create_bots_containers(self) -> None:
        y: float = 8.0
        for folder, bot_instance in self.__bot_instances.items():

            container = BotContainerComponent(parent=self.subcanvas,
                                              bot=bot_instance,
                                              x=77.0, y=y, 
                                              width=763.0, height=70.0)
            
            container.change_button_event(button='play',
                                       event=lambda bot=bot_instance: self.start_bot(bot=bot))
           
            container.change_button_event(button='settings', 
                                       event=lambda folder=folder, bot_instance=bot_instance: self.__parent.show_canvas(name='SettingCanvas',
                                                                                                       bot_folder=folder,
                                                                                                  settings=bot_instance.settings_services))
            '''
            container.change_button_event(button='delete', 
                                       event=lambda folder=folder: self.delete_bot(folder=folder))
            '''
            y += 125.0
    
    def refresh(self) -> None:
        self.subcanvas.delete("all")
        self.__parent.create_bots_folder()
        bots_folders: list[str] = [folder_name for folder_name in os.listdir(self.__parent.bots_folder_path)]
        new_instances: dict = {}
    
        for folder in bots_folders:
            try:
                module = __import__(f'bots.{folder}.main', fromlist=['Main'])
                bot = getattr(module, 'Main')
                
                if(folder in self.__bot_instances):
                    new_instances[folder] = self.__bot_instances[folder]
                else:
                    new_instances[folder] = bot()
                    
            except ModuleNotFoundError:
                messagebox.showerror(title='Main file not found', message='There is no file named main')
            except AttributeError:
                messagebox.showerror(title='Main not found', message=f'There is no Main class in {folder}')

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
        
    