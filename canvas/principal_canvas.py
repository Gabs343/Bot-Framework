import tkinter as tk
from tkinter import filedialog
import shutil
import os

from gui_factory import GUIFactory

class PrincipalCanvas(tk.Canvas): 
    def __init__(self, parent: tk.Tk, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        
        self.parent = parent
        self.bot_instances = {}
        self.gui_factory: GUIFactory = parent.gui_factory
        
        self.subcanvas = self.gui_factory.get_subcanvas(parent=self)
        self.subcanvas.place(x=75, y=75)
        
        add_btn = self.gui_factory.get_button(parent=self, icon='add', event= lambda: self.add_bot())
        add_btn.place(
            x=495.0, y=433.0,
            width=70.0, height=70.0
        )
        
        refresh_btn = self.gui_factory.get_button(parent=self, icon='refresh', event= lambda: self.refresh())
        refresh_btn.place(
            x=915.0, y=29.0,
            width=50.0, height=50.0
        )
        
        self.refresh()
        
    def refresh(self) -> None:
        self.parent.create_bots_folder()
        bots_folders = [folder_name for folder_name in os.listdir(self.parent.bots_folder_path)]
        new_instances = {}
        print(bots_folders)
        for folder in bots_folders:
            module = __import__(f'bots.{folder}.main', fromlist=['Main'])
            bot = getattr(module, 'Main')
            
            if(folder in self.bot_instances):
                new_instances[folder] = self.bot_instances[folder]
            else:
                new_instances[folder] = bot()

        self.bot_instances = new_instances
        
    def add_bot(self) -> None:
        src_bot = filedialog.askdirectory()
        shutil.move(src_bot, self.parent.bots_folder_path)
        self.refresh()