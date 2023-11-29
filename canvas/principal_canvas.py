import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os

from gui_factory import GUIFactory

class PrincipalCanvas(tk.Canvas): 
    def __init__(self, parent: tk.Tk, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        
        self.parent = parent
        self.bot_instances = {}
        self.bot_containers = []
        self.gui_factory: GUIFactory = parent.gui_factory
        
        self.subcanvas = self.gui_factory.get_subcanvas(parent=self)
        self.subcanvas.place(x=75, y=75)
        
        add_btn = self.gui_factory.get_button(parent=self, 
                                              icon='add', 
                                              event= lambda: self.add_bot())
        
        refresh_btn = self.gui_factory.get_button(parent=self, 
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
        
    def refresh(self) -> None:
        self.destroy_bots_containers()
        self.parent.create_bots_folder()
        bots_folders = [folder_name for folder_name in os.listdir(self.parent.bots_folder_path)]
        new_instances = {}
    
        for folder in bots_folders:
            module = __import__(f'bots.{folder}.main', fromlist=['Main'])
            bot = getattr(module, 'Main')
            
            if(folder in self.bot_instances):
                new_instances[folder] = self.bot_instances[folder]
            else:
                new_instances[folder] = bot()

        self.bot_instances = new_instances
        self.create_bots_containers()
        
    def add_bot(self) -> None:
        src_bot = filedialog.askdirectory()
        shutil.move(src_bot, self.parent.bots_folder_path)
        self.refresh()
        
    def create_bots_containers(self) -> None:
        y = 8.0
        for folder, bot_instance in self.bot_instances.items():
            
            container = self.gui_factory.get_bot_container(parent=self.subcanvas, 
                                                           coordinates=(77.0, y), 
                                                           bot_instance=bot_instance)
            container.set_button_event(button=1, 
                                       event=lambda folder=folder, bot_instance=bot_instance: self.parent.show_canvas(name='SettingCanvas',
                                                                                                       bot_folder=folder,
                                                                                                       settings=bot_instance.settings_services))
            container.set_button_event(button=2, 
                                       event=lambda folder=folder: self.delete_bot(folder=folder))
            self.bot_containers.append(container)
            y += 125.0
            
    def delete_bot(self, folder: str) -> None:
        msg_delete = messagebox.askquestion('Delete Bot', 'Are you sure you want to delete this bot?',
                                icon='warning')
        if(msg_delete == "yes"):
            shutil.rmtree(f'{self.parent.bots_folder_path}\\{folder}')
        self.refresh()

            
    def destroy_bots_containers(self)  -> None:
        for container in self.bot_containers:
            container.remove_gui_elements()
            
        self.bot_containers.clear()
